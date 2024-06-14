import datetime
import json
import sqlite3

import requests
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QDialog, QListWidgetItem
from bs4 import BeautifulSoup
from qfluentwidgets import (ScrollArea, ListWidget, RoundMenu, Action, FluentIcon, TitleLabel)

import Widgets

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

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

        self.reminders_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.reminders_list.customContextMenuRequested.connect(self.show_context_menu)

        self.load_todos_for_today()

    def load_todos_for_today(self):
        conn = sqlite3.connect('resources/misc/todos.db')
        cursor = conn.cursor()

        # Get today's date in the format stored in the database
        today_date = datetime.datetime.now().strftime("%a %b %d %Y")
        print(f"Loading reminders for date: {today_date}")

        # Debugging step: Print all dates in the database
        cursor.execute('SELECT DISTINCT date FROM todos')
        all_dates = cursor.fetchall()
        print("All dates in database:")
        for date in all_dates:
            print(date)

        # Fetch reminders for today's date
        cursor.execute('SELECT id, time, description, status FROM todos WHERE date = ?', (today_date,))
        todos = cursor.fetchall()
        print(f"Found {len(todos)} reminders")

        for todo_id, time, description, status in todos:
            reminder_item = QListWidgetItem(f"{time} - {description} - {status}")
            reminder_item.setData(Qt.ItemDataRole.UserRole, todo_id)  # Store the id in the item
            print(f"Loaded todo with id: {todo_id}")  # Debug: Print the loaded todo_id
            self.reminders_list.addItem(reminder_item)

        if len(todos) == 0:
            self.reminders_list.addItem(QListWidgetItem("Nothing on the agenda! Kick back and enjoy your day!"))

        conn.close()

    def show_context_menu(self, position: QPoint):
        menu = RoundMenu()
        mark_as_done_action = Action(FluentIcon.CHECKBOX, "Mark as Done", self)
        delete_action = Action(FluentIcon.DELETE, "Mark as Done & Delete", self)
        delete_action.triggered.connect(self.delete_item)
        mark_as_done_action.triggered.connect(self.mark_as_done)
        menu.addAction(mark_as_done_action)
        menu.addAction(delete_action)
        action = menu.exec(self.reminders_list.mapToGlobal(position))

        if action == delete_action:
            self.delete_item()

    def delete_item(self):
        selected_item = self.reminders_list.currentItem()
        if selected_item:
            todo_id = selected_item.data(Qt.ItemDataRole.UserRole)
            print(f"Deleting todo with id: {todo_id}")  # Debug: print the id to be deleted
            if todo_id is not None:
                self.remove_todo_from_database(todo_id)
                self.reminders_list.takeItem(self.reminders_list.row(selected_item))
            else:
                print("Error: No todo_id found for the selected item.")

    def mark_as_done(self):
        selected_item = self.reminders_list.currentItem()
        if selected_item:
            todo_id = selected_item.data(Qt.ItemDataRole.UserRole)
            if todo_id is not None:
                self.update_todo_status_in_database(todo_id)
                self.update_list_widget_item(selected_item)

    def update_todo_status_in_database(self, todo_id):
        conn = sqlite3.connect('resources/misc/todos.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE todos SET status = ? WHERE id = ?', ("Done", todo_id))
        conn.commit()
        conn.close()

    def update_list_widget_item(self, item):
        parts = item.text().rsplit(" - ", 1)  # Split on the last occurrence of " - "
        if len(parts) == 2:
            new_text = f"{parts[0]} - Done"
            item.setText(new_text)

    def remove_todo_from_database(self, todo_id):
        conn = sqlite3.connect('resources/misc/todos.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
        conn.close()
        print(f"Deleted todo with id: {todo_id} from database")


class ReminderToday(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reminders for Today")
        self.layout = QVBoxLayout(self)

        self.reminders_list = ListWidget()
        self.layout.addWidget(self.reminders_list, alignment=Qt.AlignmentFlag.AlignTop)

        self.reminders_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.reminders_list.customContextMenuRequested.connect(self.show_context_menu)

        self.load_reminders_for_today()

    def load_reminders_for_today(self):
        conn = sqlite3.connect('resources/misc/reminders.db')
        cursor = conn.cursor()

        # Get today's date in the format stored in the database
        today_date = datetime.datetime.now().strftime("%a %b %d %Y")
        print(f"Loading reminders for date: {today_date}")

        # Debugging step: Print all dates in the database
        cursor.execute('SELECT DISTINCT date FROM reminders')
        all_dates = cursor.fetchall()
        # print("All dates in database:")
        # for date in all_dates:
        # print(date)

        # Fetch reminders for today's date
        cursor.execute('SELECT id, time, description FROM reminders WHERE date = ?', (today_date,))
        todos = cursor.fetchall()
        # print(f"Found {len(todos)} reminders")

        for todo_id, time, description in todos:
            reminder_item = QListWidgetItem(f"{time} - {description}")
            reminder_item.setData(Qt.ItemDataRole.UserRole, todo_id)  # Store the id in the item
            # print(f"Loaded todo with id: {todo_id}")  # Debug: Print the loaded todo_id
            self.reminders_list.addItem(reminder_item)

        if len(todos) == 0:
            self.reminders_list.addItem(QListWidgetItem("Nothing on the agenda! Kick back and enjoy your day!"))

        conn.close()

    def show_context_menu(self, position: QPoint):
        menu = RoundMenu()
        delete_action = Action(FluentIcon.DELETE, "Mark as Done & Delete", self)
        delete_action.triggered.connect(self.delete_item)
        menu.addAction(delete_action)
        action = menu.exec(self.reminders_list.mapToGlobal(position))

    def delete_item(self):
        selected_item = self.reminders_list.currentItem()
        if selected_item:
            todo_id = selected_item.data(Qt.ItemDataRole.UserRole)
            print(f"Deleting reminder with id: {todo_id}")  # Debug: print the id to be deleted
            if todo_id is not None:
                self.remove_todo_from_database(todo_id)
                self.reminders_list.takeItem(self.reminders_list.row(selected_item))
            else:
                print("Error: No todo_id found for the selected item.")

    def remove_todo_from_database(self, todo_id):
        conn = sqlite3.connect('resources/misc/reminders.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reminders WHERE id = ?', (todo_id,))
        conn.commit()
        conn.close()
        print(f"Deleted todo with id: {todo_id} from database")


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
        try:
            if zodiac != "":
                self.header_card.setText(("<b>Today's Horoscope</b>: &#13;&#10;" + "\n" + "\n" + self.horoscope()))
            else:
                self.header_card.setText(
                    "<b>Can't find horoscope info. Make sure you have entered your Zodiac sign and you have a valid internet connection</b>:")
            self.scroll_layout.addWidget(self.header_card)
        except requests.exceptions.ConnectionError:
            self.header_card.setText(
                "<b>Make sure you have a valid internet connection</b>:")

        try:
            dob = self.parse_date(_config["dob"])
            days_rem_till_bday = self.days_until_next_birthday(dob)
        except Exception as e:
            days_rem_till_bday = "N/A"

        count_todo = self.get_number_of_todos_for_date(date_str)
        count_reminder = self.get_number_of_remainders_for_date(date_str)

        if count_todo == 0:
            self.addCard_Appointments(QIcon("resources/icons/todo.png"),
                                      "TODOs for Today", "Nothing on the agenda! Kick back and enjoy your day!")
        else:
            self.addCard_Appointments(QIcon("resources/icons/todo.png"),
                                      "TODOs for Today", f"There are {count_todo} TODO(s) for today")

        #####################################################

        if count_todo == 0:
            self.addCard_Reminders(QIcon("resources/icons/appointments.png"),
                                   "Reminders for Today", "Nothing on the agenda! Kick back and enjoy your day!")
        else:
            self.addCard_Reminders(QIcon("resources/icons/appointments.png"),
                                   "Reminders for Today", f"There are {count_reminder} Reminder(s) for today")


        spcl_title = TitleLabel()
        spcl_title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        spcl_title.setText("✨ Special Dates ✨")
        self.scroll_layout.addWidget(spcl_title, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.addCard_V(QIcon("resources/icons/cake.png"),
                       f"{days_rem_till_bday}", "days remaining till birthday")

        self.add_special_date_cards()


        self.show()

    def addCard_V(self, icon=None, title=None, content=None):
        card = Widgets.AppCard(icon, title, content, self)
        self.scroll_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def addCard_Appointments(self, icon=None, title=None, content=None):
        card = Widgets.AppointmentsCard(icon, title, content, self)
        self.scroll_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def addCard_Reminders(self, icon=None, title=None, content=None):
        card = Widgets.RemindersCard(icon, title, content, self)
        self.scroll_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def addCard_H(self, icon=None, title=None, content=None):
        card = Widgets.AppCard(icon, title, content, self)
        self.hbox_r1.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def get_number_of_todos_for_date(self, date_str):
        conn = sqlite3.connect('resources/misc/todos.db')
        cursor = conn.cursor()

        # Ensure the date format matches the actual format in the database
        date = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d").strftime("%a %b %d %Y")
        cursor.execute('SELECT COUNT(*) FROM todos WHERE date = ?', (date,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_special_dates(self):
        conn = sqlite3.connect('resources/misc/special_dates.db')
        cursor = conn.cursor()
        cursor.execute('SELECT date, reason FROM special_dates')
        special_dates = cursor.fetchall()
        conn.close()
        return special_dates

    def add_special_date_cards(self):
        special_dates = self.get_special_dates()
        today = datetime.datetime.today()

        for date_str, reason in special_dates:
            special_date = datetime.datetime.strptime(date_str, '%a %b %d %Y')
            days_until = (special_date - today).days

            if days_until >= 0:
                self.addCard_V(QIcon("resources/icons/special_day.png"),
                               f"{days_until}", f"days remaining till {reason}")

    def get_number_of_todos_for_spcl_date(self, date_str):
        conn = sqlite3.connect('resources/misc/special_dates.db')
        cursor = conn.cursor()

        # Ensure the date format matches the actual format in the database
        date = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d").strftime("%a %b %d %Y")
        cursor.execute('SELECT COUNT(*) FROM special_dates WHERE date = ?', (date,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_number_of_remainders_for_date(self, date_str):
        conn = sqlite3.connect('resources/misc/reminders.db')
        cursor = conn.cursor()

        # Ensure the date format matches the actual format in the database
        date = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d").strftime("%a %b %d %Y")
        cursor.execute('SELECT COUNT(*) FROM reminders WHERE date = ?', (date,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def today_todo(self):
        dialog = ToDoToday()
        dialog.exec()

    def today_reminders(self):
        dialog = ReminderToday()
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
