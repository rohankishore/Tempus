import json

import requests
from PyQt6.QtCore import QDate, QSize, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QCalendarWidget,
                             QLabel, QVBoxLayout, QDialog, QSpacerItem)

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

API_KEY = 'kFMc4CuIbuiw79o9q0dYwUuKAD1lhdbk'
COUNTRY = 'IN'


class FestivalDialog(QDialog):

    def __init__(self, date, festivals):
        super().__init__()
        self.initUI(date, festivals)
        self.setObjectName("Popup")
        self.setMinimumSize(QSize(500, 400))

    # self.setMaximumSize(QSize(600, 500))

    def initUI(self, date, festivals):
        vbox = QVBoxLayout(self)
        vbox.addSpacing(40)
        # vbox.addStretch()
        spacer = QSpacerItem(0, 10)
        date_label = QLabel(f"Date: {date.toString()}", self)
        date_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        vbox.addWidget(date_label, alignment=Qt.AlignmentFlag.AlignTop)
        # vbox.addSpacerItem(spacer)

        if festivals:
            for festival in festivals:
                festival_label = QLabel(f"<a href='#'>{festival['name']}</a> - {festival['description']}")
                festival_label.setOpenExternalLinks(True)
                festival_label.setFont(QFont("Consolas", 11, QFont.Weight.Bold))
                festival_label.setWordWrap(True)
                vbox.addWidget(festival_label)
        else:
            festival_label = QLabel("No festivals", self)
            vbox.addWidget(festival_label)

        self.setLayout(vbox)
        self.setWindowTitle((date.toString()))
        self.setGeometry(400, 400, 300, 150)


class Calendar(QWidget):

    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout(self)
        self.setObjectName("Calendar")
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QDate].connect(self.showDate)

        vbox.addWidget(cal)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())

        vbox.addWidget(self.lbl)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Tempus')
        self.show()

    def showDate(self, date):
        self.lbl.setText(date.toString())
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
