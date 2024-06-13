import datetime
import json

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel
from bs4 import BeautifulSoup
from qfluentwidgets import (CardWidget, IconWidget, BodyLabel, CaptionLabel, TransparentToolButton, FluentIcon,
                            RoundMenu, Action, ImageLabel, SimpleCardWidget,
                            HeaderCardWidget, HyperlinkLabel, PrimaryPushButton, TitleLabel, PillPushButton, setFont,
                            VerticalSeparator)

import Widgets

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

user_name = _config["name"]
zodiac = _config["zodiac"]
dob = _config["dob"]
today = datetime.datetime.today()
date_str = today.strftime("%Y-%m-%d") + " "
day_of_week_str = today.strftime("%A")


class Stats(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout(self)
        self.hbox_r1 = QHBoxLayout(self)
        self.setObjectName("Stats")

        self.header_card = Widgets.DateTitleCard(date=date_str, dayofweek=day_of_week_str)
        if zodiac != "":
            self.header_card.setText(("<b>Today's Horoscope</b>: &#13;&#10;" + "\n" + "\n" + self.horoscope()))
        else:
            self.header_card.setText(
                "<b>Can't find horoscope info. Make sure you have entered your Zodiac sign and you have a valid internet connection</b>:")
        self.vbox.addWidget(self.header_card)

        self.show()

        try:
            dob = self.parse_date(_config["dob"])
            delta = dob - today
            days_rem_till_bday = delta.days
        except Exception:
            pass

        self.addCard_Appointments(QIcon("resources/icons/appointments.png"),
                                  "Reminders for Today", "There are 3 reminders for today")

        self.addCard_V(QIcon("resources/icons/cake.png"),
                       f"{days_rem_till_bday}", "days remaining till birthday")

    def addCard_V(self, icon=None, title=None, content=None):
        card = Widgets.AppCard(icon, title, content, self)
        self.vbox.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def addCard_Appointments(self, icon=None, title=None, content=None):
        card = Widgets.AppointmentsCard(icon, title, content, self)
        self.vbox.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def addCard_H(self, icon=None, title=None, content=None):
        card = Widgets.AppCard(icon, title, content, self)
        self.hbox_r1.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def parse_date(self, date_str):
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')

    def horoscope(self):
        def get_horoscope(zodiac_sign: int, day: str):
            if not "-" in day:
                res = requests.get(
                    f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign}")
            else:
                day = day.replace("-", "")
                res = requests.get(
                    f"https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign={zodiac_sign}&laDate={day}")

            soup = BeautifulSoup(res.content, 'html.parser')
            data = soup.find('div', attrs={'class': 'main-horoscope'})
            return data.p.text

        zodiac_signs = {
            "Aries": 1,
            "Taurus": 2,
            "Gemini": 3,
            "Cancer": 4,
            "Leo": 5,
            "Virgo": 6,
            "Libra": 7,
            "Scorpio": 8,
            "Sagittarius": 9,
            "Capricorn": 10,
            "Aquarius": 11,
            "Pisces": 12
        }

        zodiac_res = (get_horoscope(zodiac_signs[zodiac], "today"))
        return zodiac_res