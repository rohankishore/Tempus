import datetime
import json

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from bs4 import BeautifulSoup

import Widgets

# coding:utf-8

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

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

        self.gw = Widgets.DateTitleCard(date=date_str, dayofweek=day_of_week_str)
        self.gw.setText(("<b>Today's Horoscope</b>: &#13;&#10;" + "\n" + "\n" + self.horoscope()))
        self.vbox.addWidget(self.gw)

        self.show()

        try:
            dob = self.parse_date(_config["dob"])
            delta = dob - today
            days_rem_till_bday = delta.days
        except Exception:
            pass

        self.addCard_V(f":/qfluentwidgets/images/logo.png",
                       f"{days_rem_till_bday}", "days remaining till birthday")

    def addCard_V(self, icon=None, title=None, content=None):
        card = Widgets.AppCard(icon, title, content, self)
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

        zodiac_res = ""
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

        try:
            zodiac_res = (get_horoscope(zodiac_signs[zodiac], "today"))
        except KeyError:
            pass
        return zodiac_res
