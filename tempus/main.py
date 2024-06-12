# coding:utf-8
import sys

import pycountry
import qdarktheme
from PyQt6.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QDialog, QComboBox, QLineEdit, \
    QPushButton, QMainWindow
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationBar, NavigationItemPosition, MessageBox,
                            isDarkTheme, setTheme, Theme,
                            PopUpAniStackedWidget)
from qframelesswindow import FramelessWindow, TitleBar

from Calendar import Calendar

APP_NAME = "Tempus"

import json

with open("resources/misc/config.json") as config_file:
    _config = json.load(config_file)


class Onboarding(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Onboarding')
        self.setGeometry(500, 200, 1100, 500)

        # Create main layout
        main_layout = QHBoxLayout(self)

        # Left layout
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        label1 = QLabel("Country Code")
        self.country_edit = QComboBox(self)
        self.country_edit.setPlaceholderText("Enter your country code")
        country_codes = self.fetch_country_codes()
        self.country_edit.addItems(country_codes)

        label2 = QLabel("Calendarific API Key (To view any festivals in a given date)")
        self.api_key_edit = QLineEdit(self)
        self.api_key_edit.setPlaceholderText("Enter your Calendarific API key")

        self.submit = QPushButton("Lets Go! -->")
        self.submit.clicked.connect(self.submit_details)

        self.left_layout.addWidget(self.country_edit)
        self.left_layout.addWidget(self.api_key_edit)
        self.left_layout.addWidget(self.submit, alignment=Qt.AlignmentFlag.AlignBottom)

        # Right layout
        self.right_layout = QHBoxLayout()
        self.right_layout.setContentsMargins(10, 10, 10, 10)

        # Resize the image to make it smaller
        self.right_img = QPixmap("resources/icons/Designer.png").scaled(706, 500, Qt.AspectRatioMode.IgnoreAspectRatio)
        self.right_label = QLabel()
        self.right_label.setPixmap(self.right_img)

        self.right_layout.addWidget(self.right_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Add left and right layouts to main layout
        main_layout.addLayout(self.left_layout)
        main_layout.addLayout(self.right_layout)

        # Set the dialog layout
        self.setLayout(main_layout)

    def fetch_country_codes(self):
        countries = list(pycountry.countries)
        country_codes = [country.alpha_2 for country in countries]
        return country_codes

    def submit_details(self):
        c_code = self.country_edit.currentText()
        api_Key = self.api_key_edit.text()

        _config["api-key"] = api_Key
        _config["country"] = c_code
        _config["start"] = "True"

        with open("resources/misc/config.json", "w") as config_file:
            json.dump(_config, config_file)

        self.accept()
        self.goto_app()

    def goto_app(self):
        self.accept()
        global main_window
        main_window = Window()
        main_window.start()
        main_window.show()


class StackedWidget(QFrame):
    """ Stacked widget """

    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, (QEasingCurve.Type.InQuad))

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(20, 20)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertWidget(
            1, self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(
            2, self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)  # This line adds the minBtn
        self.buttonLayout.addWidget(self.maxBtn)  # This line adds the maxBtn
        self.buttonLayout.addWidget(self.closeBtn)  # This line adds the closeBtn
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(20, 20))

    def resizeEvent(self, e):
        pass


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = StackedWidget(self)

        # create sub interface
        self.videoInterface = ""

        if _config.get("start") == "True":
            self.start()
        else:
            qdarktheme.setup_theme("dark")
            onboarding = Onboarding()
            onboarding.exec()

    def start(self):
        self.videoInterface = Calendar()
        self.initLayout()
        self.initNavigation()
        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.videoInterface, FIF.CALENDAR, 'Calendar', selectedIcon=FIF.CALENDAR)
        self.navigationBar.addItem(
            routeKey='About',
            icon=FIF.HELP,
            text='About',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.navigationBar.setCurrentItem(self.videoInterface.objectName())

    def initWindow(self):
        self.resize(1000, 600)
        self.setWindowIcon(QIcon('resources/icons/icon.png'))
        self.setWindowTitle(APP_NAME)
        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, selectedIcon=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position,
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resources/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        text_for_about = f"Heya! it's Rohan, the creator of {APP_NAME}. I hope you've enjoyed using this app as much as I enjoyed making it." + "" + "\n" + "\n" \
                                                                                                                                                            "I'm a school student and I can't earn my own money LEGALLY. So any donations will be largely appreciated. Also, if you find any bugs / have any feature requests, you can open a Issue/ Pull Request in the Repo." \
                                                                                                                                                            "You can visit GitHub by pressing the button below. You can find Ko-Fi link there :) " + "\n" + "\n" + \
                         f"Once again, thank you for using {APP_NAME}. Please consider giving it a star ⭐ as it will largely motivate me to create more of such apps. Also do consider giving me a follow ;) "
        w = MessageBox(
            APP_NAME,
            text_for_about,
            self
        )
        w.yesButton.setText('GitHub')
        w.cancelButton.setText('Return')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/rohankishore/Tempus"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    qdarktheme.enable_hi_dpi()
    w = Window()
    qdarktheme.setup_theme("dark")
    w.show()
    sys.exit(app.exec())
