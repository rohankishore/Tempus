import json
import sqlite3

import requests
from PyQt6.QtCore import QDate, QSize, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QCalendarWidget,
                             QLabel, QVBoxLayout, QDialog, QSpacerItem, QHBoxLayout,
                             QListWidgetItem, QInputDialog)
from qfluentwidgets import (FluentIcon,
                            PushButton,
                            ListWidget, LineEdit)

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

# API_KEY = 'kFMc4CuIbuiw79o9q0dYwUuKAD1lhdbk'
# COUNTRY = 'IN'


API_KEY = _config["api-key"]
COUNTRY = _config['country']


class TodoDialog(QDialog):
    def __init__(self, date):
        super().__init__()
        self.date = date.toString()

        # Set up the database connection
        self.conn = sqlite3.connect('resources/misc/todos.db')
        self.cursor = self.conn.cursor()

        # Create a table to store todos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                description TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

        # Set up the dialog layout
        self.setWindowTitle(f"Todo List for {self.date}")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout(self)

        # Create the QListWidget
        self.list_widget = ListWidget()
        self.layout.addWidget(self.list_widget)

        # Create the add button
        self.add_button = PushButton()
        self.add_button.setIcon(FluentIcon.ADD)
        self.add_button.setText("Add Item")
        self.layout.addWidget(self.add_button)

        # Connect the button's clicked signal to the add_item method
        self.add_button.clicked.connect(self.add_item)

        # Load existing todos for the given date
        self.load_todos()

    def load_todos(self):
        self.cursor.execute('SELECT time, description, status FROM todos WHERE date = ?', (self.date,))
        todos = self.cursor.fetchall()
        for time, description, status in todos:
            self.add_item_to_list(time, description, status)

    def add_item(self):
        # Create a new list widget item
        item = QListWidgetItem()
        self.list_widget.addItem(item)

        # Create a widget to hold the line edits and save button
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(0, 0, 0, 0)

        # Create line edits for time, description, and status
        line_edit_time = LineEdit()
        line_edit_time.setPlaceholderText("Time")
        line_edit_description = LineEdit()
        line_edit_description.setPlaceholderText("Description")
        line_edit_status = LineEdit()
        line_edit_status.setPlaceholderText("Status")

        # Create a save button
        save_button = PushButton()
        save_button.setText("✔️")
        save_button.clicked.connect(
            lambda: self.save_item(item, line_edit_time, line_edit_description, line_edit_status))

        # Add the line edits and save button to the item layout
        item_layout.addWidget(line_edit_time)
        item_layout.addWidget(line_edit_description)
        item_layout.addWidget(line_edit_status)
        item_layout.addWidget(save_button)

        # Set the item widget to the QListWidgetItem
        self.list_widget.setItemWidget(item, item_widget)

        # Set focus to the first QLineEdit to start editing
        line_edit_time.setFocus()

    def save_item(self, item, line_edit_time, line_edit_description, line_edit_status):
        time = line_edit_time.text()
        description = line_edit_description.text()
        status = line_edit_status.text()
        if time and description and status:
            self.add_todo(self.date, time, description, status)
            self.add_item_to_list(time, description, status)
            self.list_widget.takeItem(self.list_widget.row(item))  # Remove the editable item

    def add_item_to_list(self, time, description, status):
        # Create a new list widget item with the provided details
        item = QListWidgetItem(f"{time} - {description} - {status}")
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.list_widget.addItem(item)

    def add_todo(self, date, time, description, status):
        self.cursor.execute('INSERT INTO todos (date, time, description, status) VALUES (?, ?, ?, ?)',
                            (date, time, description, status))
        self.conn.commit()


class FestivalDialog(QDialog):

    def __init__(self, date, festivals):
        super().__init__()
        self.initUI(date, festivals)
        self.setObjectName("Popup")
        self.setMinimumSize(QSize(500, 400))
        self.date = date

    # self.setMaximumSize(QSize(600, 500))

    def initUI(self, date, festivals):
        vbox = QVBoxLayout(self)
        vbox.addSpacing(40)

        hbox = QHBoxLayout(self)
        vbox.addLayout(hbox)

        spacer = QSpacerItem(0, 10)
        date_label = QLabel(f"Date: {date.toString()}", self)
        date_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        vbox.addWidget(date_label, alignment=Qt.AlignmentFlag.AlignTop)

        festival_label = QLabel("")
        festival_label.setFont(QFont("Consolas", 11, QFont.Weight.Bold))
        festival_label.setWordWrap(True)
        festival_label.setOpenExternalLinks(True)

        add_todo_button = PushButton()
        add_todo_button.clicked.connect(self.add_todo)
        add_todo_button.setText("Add TODOs ➕")

        mark_remainder_button = PushButton()
        mark_remainder_button.clicked.connect(self.add_remainder)
        mark_remainder_button.setText("Add Reminder 🎗️")

        mark_special_button = PushButton()
        mark_special_button.setText("Mark as Special ✨")
        mark_special_button.clicked.connect(self.mark_special)

        vbox.addWidget(festival_label, alignment=Qt.AlignmentFlag.AlignTop)
        hbox.addWidget(add_todo_button, alignment=Qt.AlignmentFlag.AlignTop)
        hbox.addWidget(mark_remainder_button, alignment=Qt.AlignmentFlag.AlignTop)
        vbox.addWidget(mark_special_button)

        if festivals:
            for festival in festivals:
                text = f"<a href='#'>{festival['name']}</a> - {festival['description']}"
                festival_label.setText(text)
        else:
            festival_label = QLabel(
                "No festivals found. This could be because you haven't entered Calendarific API Key and Country."
                "You can enter it in Settings.", self)
            festival_label.setWordWrap(True)
            vbox.addWidget(festival_label)

        self.setLayout(vbox)
        self.setWindowTitle((date.toString()))
        self.setGeometry(400, 400, 300, 150)

    def add_todo(self):
        dialog = TodoDialog(self.date)
        dialog.exec()

    def add_remainder(self):
        dialog = ReminderDialog(self.date)
        dialog.exec()

    def mark_special(self):
        dialog = SpecialDateDialog(self.date)
        dialog.exec()


class ReminderDialog(QDialog):
    def __init__(self, date):
        super().__init__()
        self.date = date.toString()

        # Set up the database connection
        self.conn = sqlite3.connect('resources/misc/reminders.db')
        self.cursor = self.conn.cursor()

        # Create a table to store reminders
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                description TEXT
            )
        ''')
        self.conn.commit()

        # Set up the dialog layout
        self.setWindowTitle(f"Reminders for {self.date}")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout(self)

        # Create the QListWidget
        self.list_widget = ListWidget()
        self.layout.addWidget(self.list_widget)

        # Create the add button
        self.add_button = PushButton()
        self.add_button.setIcon(FluentIcon.ADD)
        self.add_button.setText("Add Reminder")
        self.layout.addWidget(self.add_button)

        # Connect the button's clicked signal to the add_reminder method
        self.add_button.clicked.connect(self.add_reminder)

        # Load existing reminders for the given date
        self.load_reminders()

    def load_reminders(self):
        self.cursor.execute('SELECT time, description FROM reminders WHERE date = ?', (self.date,))
        reminders = self.cursor.fetchall()
        for time, description in reminders:
            self.add_item_to_list(time, description)

    def add_reminder(self):
        # Create a new list widget item
        item = QListWidgetItem()
        self.list_widget.addItem(item)

        # Create a widget to hold the line edits and save button
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(0, 0, 0, 0)

        # Create line edits for time and description
        line_edit_time = LineEdit()
        line_edit_time.setPlaceholderText("Time")
        line_edit_description = LineEdit()
        line_edit_description.setPlaceholderText("Description")

        # Create a save button
        save_button = PushButton()
        save_button.setText("✔️")
        save_button.clicked.connect(lambda: self.save_reminder(item, line_edit_time, line_edit_description))

        # Add the line edits and save button to the item layout
        item_layout.addWidget(line_edit_time)
        item_layout.addWidget(line_edit_description)
        item_layout.addWidget(save_button)

        # Set the item widget to the QListWidgetItem
        self.list_widget.setItemWidget(item, item_widget)

        # Set focus to the first QLineEdit to start editing
        line_edit_time.setFocus()

    def save_reminder(self, item, line_edit_time, line_edit_description):
        time = line_edit_time.text()
        description = line_edit_description.text()
        if time and description:
            self.add_reminder_to_db(self.date, time, description)
            self.add_item_to_list(time, description)
            self.list_widget.takeItem(self.list_widget.row(item))  # Remove the editable item

    def add_item_to_list(self, time, description):
        # Create a new list widget item with the provided details
        item = QListWidgetItem(f"{time} - {description}")
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.list_widget.addItem(item)

    def add_reminder_to_db(self, date, time, description):
        self.cursor.execute('INSERT INTO reminders (date, time, description) VALUES (?, ?, ?)',
                            (date, time, description))
        self.conn.commit()


class SpecialDateDialog(QDialog):
    def __init__(self, date):
        super().__init__()
        self.date = date.toString()

        # Set up the database connection
        self.conn = sqlite3.connect('resources/misc/special_dates.db')
        self.cursor = self.conn.cursor()

        # Create a table to store special dates
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS special_dates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                reason TEXT
            )
        ''')
        self.conn.commit()

        # Set up the dialog layout
        self.setWindowTitle(f"Special Date: {self.date}")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout(self)

        # Create the reason input
        self.reason_input = LineEdit()
        self.reason_input.setPlaceholderText("Reason for marking this date as special")
        self.layout.addWidget(self.reason_input)

        # Create the save button
        self.save_button = PushButton()
        self.save_button.setIcon(FluentIcon.SAVE)
        self.save_button.setText("Save")
        self.layout.addWidget(self.save_button)

        # Connect the button's clicked signal to the save_special_date method
        self.save_button.clicked.connect(self.save_special_date)

        # Load existing special date if any
        self.load_special_date()

    def load_special_date(self):
        self.cursor.execute('SELECT reason FROM special_dates WHERE date = ?', (self.date,))
        result = self.cursor.fetchone()
        if result:
            self.reason_input.setText(result[0])

    def save_special_date(self):
        reason = self.reason_input.text()
        if reason:
            self.cursor.execute('REPLACE INTO special_dates (date, reason) VALUES (?, ?)', (self.date, reason))
            self.conn.commit()
            self.close()


class Calendar(QCalendarWidget):
    def __init__(self):
        super().__init__()
        self.setGridVisible(True)
        self.clicked[QDate].connect(self.showDate)
        self.hovered_date = None

    def event(self, event):
        if event.type() == event.Type.MouseMove:
            pos = event.pos()
            date = self.dateAt(pos)
            if date != self.hovered_date:
                self.hovered_date = date
                self.update()
        return super().event(event)

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        if date == self.hovered_date:
            painter.fillRect(rect, Qt.GlobalColor.lightGray)

    def showDate(self, date):
        date_str = date.toString("yyyy-MM-dd")
        festivals = self.getFestivals(date_str)
        dialog = FestivalDialog(date, festivals)
        dialog.exec()

    def getFestivals(self, date):
        url = f'https://calendarific.com/api/v2/holidays'
        params = {
            'api_key': API_KEY,
            'country': COUNTRY,
            'year': date.split('-')[0],
            'month': date.split('-')[1],
            'day': date.split('-')[2]
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['response']['holidays']
        else:
            return []


class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout(self)
        self.setObjectName("Calendar")
        self.calendar = Calendar()
        vbox.addWidget(self.calendar)
        self.lbl = QLabel(self)
        date = self.calendar.selectedDate()
        self.lbl.setText(date.toString())
        vbox.addWidget(self.lbl)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Tempus')
        self.show()
