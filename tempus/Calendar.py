#!/usr/bin/python

"""
ZetCode PyQt6 tutorial

This example shows a QCalendarWidget widget with a popup dialog displaying festival information fetched from an API.

Author: Jan Bodnar
Modified by: Your Name
Website: zetcode.com
"""

from PyQt6.QtWidgets import (QWidget, QCalendarWidget,
                             QLabel, QApplication, QVBoxLayout, QDialog)
from PyQt6.QtCore import QDate
import sys
import requests


API_KEY = 'kFMc4CuIbuiw79o9q0dYwUuKAD1lhdbk'  # Replace with your Calendarific API key
COUNTRY = 'US'  # Set your country code


class FestivalDialog(QDialog):

    def __init__(self, date, festivals):
        super().__init__()
        self.initUI(date, festivals)
        self.setObjectName("Popup")

    def initUI(self, date, festivals):
        vbox = QVBoxLayout(self)

        date_label = QLabel(f"Date: {date.toString()}", self)
        vbox.addWidget(date_label)

        if festivals:
            for festival in festivals:
                festival_label = QLabel(f"Festival: {festival['name']} - {festival['description']}", self)
                vbox.addWidget(festival_label)
        else:
            festival_label = QLabel("No festivals", self)
            vbox.addWidget(festival_label)

        self.setLayout(vbox)
        self.setWindowTitle("Festival Information")
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
