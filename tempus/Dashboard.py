import datetime
import json
import sqlite3

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QDialog, QListWidgetItem
from bs4 import BeautifulSoup
from qfluentwidgets import (ScrollArea, ListWidget)

import Widgets

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

user_name = _config["name"]
zodiac = _config["zodiac"]
dob = _config["dob"]
today = datetime.datetime.today()
date_str = today.strftime("%Y-%m-%d") + " "
day_of_week_str = today.strftime("%A")


class ToDoToday(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TODOs for Today")
        self.layout = QVBoxLayout(self)

        self.reminders_list = ListWidget()
        self.layout.addWidget(self.reminders_list, alignment=Qt.AlignmentFlag.AlignTop)

        self.load_reminders_for_today()

    def load_reminders_for_today(self):
        conn = sqlite3.connect('resources/misc/todos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT time, description, status FROM todos WHERE date = ?', (date_str.strip(),))
        todos = cursor.fetchall()
        for time, description, status in todos:
            reminder_item = QListWidgetItem(f"{time} - {description} - {status}")
            self.reminders_list.addItem(reminder_item)
        conn.close()


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)

        # Initialize ScrollArea and set it as the main layout's widget
        self.scroll_area = ScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        # Add ScrollArea to the main layout
        self.main_layout.addWidget(self.scroll_area)

        self.setObjectName("Home")

        self.header_card = Widgets.DateTitleCard(date=date_str, dayofweek=day_of_week_str)
        if zodiac != "":
            self.header_card.setText(("<b>Today's Horoscope</b>: &#13;&#10;" + "\n" + "\n" + self.horoscope()))
        else:
            self.header_card.setText(
                "<b>Can't find horoscope info. Make sure you have entered your Zodiac sign and you have a valid internet connection</b>:")
        self.scroll_layout.addWidget(self.header_card)

        try:
            dob = self.parse_date(_config["dob"])
            days_rem_till_bday = self.days_until_next_birthday(dob)
        except Exception as e:
            days_rem_till_bday = "N/A"

        count = self.get_number_of_todos_for_date(date_str)

        if count == 0:
            self.addCard_Appointments(QIcon("resources/icons/appointments.png"),
                                      "Reminders for Today", "Nothing on the agenda! Kick back and enjoy your day!")
        else:
            self.addCard_Appointments(QIcon("resources/icons/appointments.png"),
                                      "Reminders for Today", f"There are {count} reminders for today")

        self.addCard_V(QIcon("resources/icons/cake.png"),
                       f"{days_rem_till_bday}", "days remaining till birthday")

        self.show()

    def addCard_V(self, icon=None, title=None, content=None):
        card = Widgets.AppCard(icon, title, content, self)
        self.scroll_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def addCard_Appointments(self, icon=None, title=None, content=None):
        card = Widgets.AppointmentsCard(icon, title, content, self)
        self.scroll_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def addCard_H(self, icon=None, title=None, content=None):
        card = Widgets.AppCard(icon, title, content, self)
        self.hbox_r1.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def get_number_of_todos_for_date(self, date):
        conn = sqlite3.connect('resources/misc/todos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM todos WHERE date = ?', (date,))
        self.count = cursor.fetchone()[0]
        conn.close()
        return self.count

    def today_todo(self):
        dialog = ToDoToday()
        dialog.exec()

    def days_until_next_birthday(self, dob):
        today = datetime.datetime.today()
        next_birthday = dob.replace(year=today.year)
        if today > next_birthday:
            next_birthday = dob.replace(year=today.year + 1)
        return (next_birthday - today).days

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
