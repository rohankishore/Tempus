import json

import pycountry
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import (PushButton,
                            LineEdit, CaptionLabel, HorizontalSeparator)

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

user_name = _config["name"]
zodiac = _config["zodiac"]
dob = _config["dob"]
api = _config["api-key"]
country = _config["country"]


# today = datetime.datetime.today()
# date_str = today.strftime("%Y-%m-%d") + " "
# day_of_week_str = today.strftime("%A")

class SettingInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        seperator = HorizontalSeparator(self)

        name_layout = QHBoxLayout(self)
        self.layout.addLayout(name_layout)

        dob_layout = QHBoxLayout(self)
        self.layout.addLayout(dob_layout)

        self.layout.addWidget(seperator)

        api_layout = QHBoxLayout(self)
        self.layout.addLayout(api_layout)

        country_layout = QHBoxLayout(self)
        self.layout.addLayout(country_layout)

        zodiac_layout = QHBoxLayout(self)
        self.layout.addLayout(zodiac_layout)

        bottom_layout = QHBoxLayout(self)
        self.layout.addLayout(bottom_layout)

        self.name_label = CaptionLabel(self)
        self.name_label.setText("Name")
        self.name_entry = LineEdit(self)
        self.name_entry.setText(user_name)

        self.dob_label = CaptionLabel(self)
        self.dob_label.setText("DOB  ")
        self.dob_entry = LineEdit(self)
        self.dob_entry.setText(dob)

        self.api_label = CaptionLabel(self)
        self.api_label.setText("Calendarific API Key")
        self.api_entry = LineEdit(self)
        self.api_entry.setText(api)

        country_label = CaptionLabel(self)
        country_label.setText("Country")
        self.country_select = QComboBox(self)
        country_codes = self.fetch_country_codes()
        self.country_select.addItems(country_codes)
        self.country_select.setCurrentText(country)

        zodiac_label = CaptionLabel(self)
        zodiac_label.setText("Zodiac Sign")
        self.zodiac_select = QComboBox(self)
        zodiacs_list = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        self.zodiac_select.addItems(zodiacs_list)
        self.zodiac_select.setCurrentText(zodiac)

        self.submit_buttom = PushButton()
        self.submit_buttom.setText("Save Settings")
        bottom_layout.addWidget(self.submit_buttom, alignment=Qt.AlignmentFlag.AlignBottom)

        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_entry)
        dob_layout.addWidget(self.dob_label)
        dob_layout.addWidget(self.dob_entry)
        api_layout.addWidget(self.api_label)
        api_layout.addWidget(self.api_entry)
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_select)
        zodiac_layout.addWidget(zodiac_label)
        zodiac_layout.addWidget(self.zodiac_select)

    def fetch_country_codes(self):
        countries = list(pycountry.countries)
        country_codes = [country.alpha_2 for country in countries]
        return country_codes
