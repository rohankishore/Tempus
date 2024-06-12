import datetime
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
from quote import quote
import pycountry
import qdarktheme
from PyQt6.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl, QPoint
from PyQt6.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QDialog, QComboBox, QLineEdit, \
    QPushButton, QMainWindow, QWidget


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout(self)
        self.hbox_r1 = QHBoxLayout(self)
        self.setObjectName("Calendar")
        self.show()

        today = datetime.datetime.today()
        date_str = today.strftime("%Y-%m-%d") + " "
        day_of_week_str = today.strftime("%A")

        self.addCard(f":/qfluentwidgets/images/logo.png",
                     f"Today is {date_str}", day_of_week_str)


    def addCard(self, icon=None, title=None, content=None):
        card = AppCard(icon, title, content, self)
        self.vbox.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)


class AppCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        #self.openButton = PushButton('打开', self)
        # self.moreButton = TransparentToolButton(FluentIcon.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        #self.openButton.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        # self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignmentFlag.AlignRight)
        # self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        #self.moreButton.setFixedSize(32, 32)
        #self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FluentIcon.SHARE, '共享', self))
        menu.addAction(Action(FluentIcon.CHAT, '写评论', self))
        menu.addAction(Action(FluentIcon.PIN, '固定到任务栏', self))

        #x = (self.moreButton.width() - menu.width()) // 2 + 10
        #pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        #menu.exec(pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setTheme(Theme.DARK)  # Set the theme to light
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
