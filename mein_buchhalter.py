#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtWidgets, QtCore
from menu_languages.menulanguages import MenuLanguages
from sql_handler.sql_handler import SqlHandler


settings = QtCore.QSettings('@zmv', 'Buchhalter')
if settings.contains('Language'):
    menu_language = settings.value('Language')
else:
    menu_language = 'en'
    settings.setValue('Language', menu_language)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        menu_bar = self.menuBar()
        self.set_interface_language(menu_language)
        self.db_handler = SqlHandler(self.app_dir)

    def set_interface_language(self, language):
        if language == 'en':
            self.interface_language = MenuLanguages.en
        else:
            self.interface_language = MenuLanguages.ru
        settings.setValue('Language', language)

    def check_db(self):
        if not self.db_handler.is_db_available():
            self.db_handler.create_db()
        else:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Mein Buchhalter")
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())

