# coding:utf-8

from PyQt6.QtCore import Qt, QUrl, QSize, QPoint
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import (CardWidget, IconWidget, BodyLabel, CaptionLabel, TransparentToolButton, FluentIcon,
                            RoundMenu, Action, ImageLabel, SimpleCardWidget,
                            HeaderCardWidget, HyperlinkLabel, PrimaryPushButton, TitleLabel, PillPushButton, setFont,
                            VerticalSeparator)


class AppCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        # self.openButton = PushButton('打开', self)
        # self.moreButton = TransparentToolButton(FluentIcon.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        # self.openButton.setFixedWidth(120)

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

        # self.moreButton.setFixedSize(32, 32)
        # self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FluentIcon.SHARE, '共享', self))
        menu.addAction(Action(FluentIcon.CHAT, '写评论', self))
        menu.addAction(Action(FluentIcon.PIN, '固定到任务栏', self))

        # x = (self.moreButton.width() - menu.width()) // 2 + 10
        # pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        # menu.exec(pos)


class AppointmentsCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        # self.openButton = PushButton('', self)
        # self.openButton.setIcon(FluentIcon.RIGHT_ARROW)
        self.moreButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        self.parent = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        # self.openButton.setFixedWidth(120)

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
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        view_todays_todo = Action(FluentIcon.VIEW, "View Today's TODOs", self)
        view_todays_todo.triggered.connect(self.parent.today_todo)
        menu.addAction(view_todays_todo)

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)

        #def onMoreButtonClicked(self):
         #   self.parent.today_todo()

class RemindersCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.moreButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        self.parent = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        # self.openButton.setFixedWidth(120)

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
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        view_todays_reminders = Action(FluentIcon.VIEW, "View Today's Reminders", self)
        view_todays_reminders.triggered.connect(self.parent.today_reminders)
        menu.addAction(view_todays_reminders)

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)

        #def onMoreButtonClicked(self):
         #   self.parent.today_todo()

class DateTitleCard(HeaderCardWidget):
    def __init__(self, date, dayofweek, parent=None):
        super().__init__(parent)
        self.descriptionLabel = BodyLabel('', self)

        self.descriptionLabel.setWordWrap(True)
        self.viewLayout.addWidget(self.descriptionLabel)
        self.setTitle(f"Today is {date}, "f" {dayofweek}")

    def setText(self, text):
        self.descriptionLabel.setText(text)


class StatsCard(HeaderCardWidget):
    def __init__(self, date, dayofweek, parent=None):
        super().__init__(parent)
        self.descriptionLabel = BodyLabel('', self)

        self.descriptionLabel.setWordWrap(True)
        self.viewLayout.addWidget(self.descriptionLabel)
        self.setTitle("Some Fun Stats")

    def setText(self, text):
        self.descriptionLabel.setText(text)


class AppInfoCard(SimpleCardWidget):
    """ App information card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iconLabel = ImageLabel(":/qfluentwidgets/images/logo.png", self)
        self.iconLabel.setBorderRadius(8, 8, 8, 8)
        self.iconLabel.scaledToWidth(120)

        self.nameLabel = TitleLabel('QFluentWidgets', self)
        self.installButton = PrimaryPushButton('安装', self)
        self.companyLabel = HyperlinkLabel(
            QUrl('https://github.com/zhiyiYo/PyQt-Fluent-Widgets'), 'Shokokawaii Inc.', self)
        self.installButton.setFixedWidth(160)

        self.separator = VerticalSeparator(self)

        self.descriptionLabel = BodyLabel(
            'PyQt-Fluent-Widgets 是一个基于 PyQt/PySide 的 Fluent Design 风格组件库，包含许多美观实用的组件，支持亮暗主题无缝切换和自定义主题色，帮助开发者快速实现美观优雅的现代化界面。',
            self)
        self.descriptionLabel.setWordWrap(True)

        self.tagButton = PillPushButton('组件库', self)
        self.tagButton.setCheckable(False)
        setFont(self.tagButton, 12)
        self.tagButton.setFixedSize(80, 32)

        self.shareButton = TransparentToolButton(FluentIcon.SHARE, self)
        self.shareButton.setFixedSize(32, 32)
        self.shareButton.setIconSize(QSize(14, 14))

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.initLayout()

    def initLayout(self):
        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addWidget(self.iconLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        # name label and install button
        self.vBoxLayout.addLayout(self.topLayout)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.addWidget(self.nameLabel)
        self.topLayout.addWidget(self.installButton, 0, Qt.AlignmentFlag.AlignRight)

        # company label
        self.vBoxLayout.addSpacing(3)
        self.vBoxLayout.addWidget(self.companyLabel)

        # statistics widgets
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addLayout(self.statisticsLayout)
        self.statisticsLayout.setContentsMargins(0, 0, 0, 0)
        self.statisticsLayout.setSpacing(10)
        self.statisticsLayout.addWidget(self.separator)

        # description label
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.descriptionLabel)

        # button
        self.vBoxLayout.addSpacing(12)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.buttonLayout)
