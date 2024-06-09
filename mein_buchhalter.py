#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtWidgets, QtCore
from menu_languages.menulanguages import MenuLanguages
from sql_handler.sql_handler import SqlHandler
from central_widget import CentralWidget
from tools.date_time_tool import get_current_date
from tools.my_logger import logger


settings = QtCore.QSettings('@zmv', 'Buchhalter')
if settings.contains('Language'):
    menu_language = settings.value('Language')
else:
    menu_language = 'en'
    settings.setValue('Language', menu_language)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        menu_bar = self.menuBar()
        self.set_interface_language(menu_language)
        self.db_handler = SqlHandler(self.app_dir)
        self.check_db()
        self.view = CentralWidget(self.interface_language, self.db_handler)
        self.view.start_screen()
        self.setCentralWidget(self.view)
        self.view.btn_close.clicked.connect(self.close)
        self.status_bar = self.statusBar()
        self.show_current_date()

    def set_interface_language(self, language: str):
        if language == 'en':
            self.interface_language = MenuLanguages.en
        else:
            self.interface_language = MenuLanguages.ru
        settings.setValue('Language', language)

    def check_db(self):
        if not self.db_handler.is_db_available():
            logger.info('DB is not exist')
            self.db_handler.create_db()
        else:
            logger.info('DB is available')

    def show_current_date(self):
        label_date = QtWidgets.QLabel(get_current_date())
        label_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.status_bar.addPermanentWidget(label_date)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Mein Buchhalter")
    window.resize(250, 150)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())

