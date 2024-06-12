import datetime
import json
from xml import etree

import requests
from bs4 import BeautifulSoup
from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, FluentIcon, RoundMenu, Action, ElevatedCardWidget,
                            ImageLabel, isDarkTheme, FlowLayout, MSFluentTitleBar, SimpleCardWidget,
                            HeaderCardWidget, InfoBarIcon, HyperlinkLabel, HorizontalFlipView,
                            PrimaryPushButton, TitleLabel, PillPushButton, setFont, SingleDirectionScrollArea,
                            VerticalSeparator, MSFluentWindow, NavigationItemPosition)
# coding:utf-8
import sys
import Widgets
from quote import quote
import pycountry
import qdarktheme
from PyQt6.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl, QPoint, QSize
from PyQt6.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QDialog, QComboBox, QLineEdit, \
    QPushButton, QMainWindow, QWidget

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

zodiac = _config["zodiac"]
dob = _config["dob"]
today = datetime.datetime.today()
date_str = today.strftime("%Y-%m-%d") + " "
day_of_week_str = today.strftime("%A")


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout(self)
        self.hbox_r1 = QHBoxLayout(self)
        self.setObjectName("Calendar")

        self.gw = Widgets.DescriptionCard(date=date_str, dayofweek=day_of_week_str)
        self.gw.setText("tee")
        self.vbox.addWidget(self.gw)

        self.show()

        try:
            dob = self.parse_date(_config["dob"])
            delta = dob - today
            days_rem_till_bday = delta.days
        except Exception:
            pass

        self.addCard_V(f":/qfluentwidgets/images/logo.png",
                       f"Today is {date_str}", day_of_week_str)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setTheme(Theme.DARK)  # Set the theme to light
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
