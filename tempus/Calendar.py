import json
import sqlite3

import requests
from PyQt6.QtCore import QDate, QSize, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QCalendarWidget,
                             QLabel, QVBoxLayout, QDialog, QSpacerItem, QHBoxLayout,
                             QListWidgetItem)
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
        save_button.setText("✅")
        save_button.clicked.connect(lambda: self.save_item(item, line_edit_time, line_edit_description, line_edit_status))

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
        add_todo_button.setText("Add TODOs / Reminders")

        vbox.addWidget(festival_label, alignment=Qt.AlignmentFlag.AlignTop)
        hbox.addWidget(add_todo_button, alignment=Qt.AlignmentFlag.AlignTop)

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
