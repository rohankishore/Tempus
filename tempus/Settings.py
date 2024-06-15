import json

import pycountry
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)

zodiac = _config["zodiac"]
dob = _config["dob"]
api = _config["api-key"]
country = _config["country"]
def_page = _config["def-page"]


class SettingInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setObjectName("Settings")

        dob_layout = QHBoxLayout()
        self.layout.addLayout(dob_layout)

        api_layout = QHBoxLayout()
        self.layout.addLayout(api_layout)

        country_layout = QHBoxLayout()
        self.layout.addLayout(country_layout)

        zodiac_layout = QHBoxLayout()
        self.layout.addLayout(zodiac_layout)

        label_layout = QHBoxLayout()
        self.layout.addLayout(label_layout)

        bottom_layout = QHBoxLayout()
        self.layout.addLayout(bottom_layout)

        self.dob_label = QLabel(self)
        self.dob_label.setText("DOB")
        self.dob_entry = QLineEdit(self)
        self.dob_entry.setText(dob)

        self.api_label = QLabel(self)
        self.api_label.setText("Calendarific API Key")
        self.api_entry = QLineEdit(self)
        self.api_entry.setText(api)

        country_label = QLabel(self)
        country_label.setText("Country")
        self.country_select = QComboBox(self)
        country_codes = self.fetch_country_codes()
        self.country_select.addItems(country_codes)
        self.country_select.setCurrentText(country)

        zodiac_label = QLabel(self)
        zodiac_label.setText("Zodiac Sign")
        self.zodiac_select = QComboBox(self)
        zodiacs_list = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        self.zodiac_select.addItems(zodiacs_list)
        self.zodiac_select.setCurrentText(zodiac)

        discl_label = QLabel("<b><i>*Please note that Calendarific API is limited to 500 requests per month. So you may have to"
                             "change your API keys once in a while.</i></b>")
        discl_label.setWordWrap(True)

        self.submit_button = QPushButton(self)
        self.submit_button.setText("Save Settings")
        self.submit_button.clicked.connect(self.submit_settings)
        bottom_layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignBottom)

        dob_layout.addWidget(self.dob_label)
        dob_layout.addWidget(self.dob_entry)
        api_layout.addWidget(self.api_label)
        api_layout.addWidget(self.api_entry)
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_select)
        zodiac_layout.addWidget(zodiac_label)
        zodiac_layout.addWidget(self.zodiac_select)
        label_layout.addWidget(discl_label)

    def fetch_country_codes(self):
        countries = list(pycountry.countries)
        country_codes = [country.alpha_2 for country in countries]
        return country_codes

    def submit_settings(self):
        _config["api-key"] = self.api_entry.text()
        _config["country"] = self.country_select.currentText()
        _config["zodiac"] = self.zodiac_select.currentText()
        _config["dob"] = self.dob_entry.text()

        try:
            print("Before saving:", _config)
            with open("resources/misc/config.json", "w") as json_file:
                json.dump(_config, json_file)
            #with open("resources/misc/config.json", "w") as config_file:
            #    json.dump(_config, config_file)
            print("Settings saved successfully")
            print("After saving:", _config)  # Debug statement
        except Exception as e:
            print(f"Failed to save settings: {e}")
