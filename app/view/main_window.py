# coding: utf-8
from PyQt6.QtCore import QUrl, QSize, QTimer
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtWidgets import QApplication

from qfluentwidgets import (
    NavigationItemPosition,
    FluentWindow,
    SplashScreen,
    SystemThemeListener,
    isDarkTheme,
)
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface

from ..common.config import ZH_SUPPORT_URL, EN_SUPPORT_URL, cfg
from ..common.signal_bus import signalBus

from .setting_interface import SettingInterface
from .xhs_interface import XhsInterface
from .dy_interface import DyInterface
from .ks_interface import KsInterface
from .bz_interface import BzInterface
from .wb_interface import WbInterface
from .tb_interface import TbInterface


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        # create system theme listener
        self.themeListener = SystemThemeListener(self)

        # create sub interface
        self.xhsInterface = XhsInterface()
        self.dyInterface = DyInterface()
        self.ksInterface = KsInterface()
        self.bzInterface = BzInterface()
        self.wbInterface = WbInterface()
        self.tbInterface = TbInterface()

        self.settingInterface = SettingInterface()

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

        # start theme listener
        self.themeListener.start()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(
            self.xhsInterface, QIcon("app/resource/images/icons/小红书.svg"), "小红书"
        )
        self.addSubInterface(
            self.dyInterface, QIcon("app/resource/images/icons/抖音.svg"), "抖音"
        )
        self.addSubInterface(
            self.ksInterface, QIcon("app/resource/images/icons/快手.svg"), "快手"
        )
        self.addSubInterface(
            self.bzInterface, QIcon("app/resource/images/icons/B站.svg"), "B站"
        )
        self.addSubInterface(
            self.wbInterface, QIcon("app/resource/images/icons/微博.svg"), "微博"
        )
        self.addSubInterface(
            self.tbInterface,
            QIcon("app/resource/images/icons/百度贴吧.svg"),
            "百度贴吧",
        )

        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            self.tr("Settings"),
            NavigationItemPosition.BOTTOM,
        )

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        # self.setWindowIcon(QIcon(":/gallery/images/logo1.png"))
        self.setWindowIcon(QIcon("app/resource/images/logo1.png"))
        self.setWindowTitle("🔥 自媒体平台爬虫🕷️MediaCrawler🔥")

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(ZH_SUPPORT_URL))
        else:
            QDesktopServices.openUrl(QUrl(EN_SUPPORT_URL))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "splashScreen"):
            self.splashScreen.resize(self.size())

    def closeEvent(self, e):
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()

        # retry
        if self.isMicaEffectEnabled():
            QTimer.singleShot(
                100,
                lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()),
            )

    def switchToSample(self, routeKey, index):
        """switch to sample"""
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
