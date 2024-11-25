#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtWidgets, QtCore
from menu_languages.menulanguages import MenuLanguages
from sql_handler.sql_handler import SqlHandler
from widgets.day_balance_view import DayBalanceView
from widgets.month_balance_view import MonthBalanceView
from widgets.month_income_view import MonthIncomeView
from widgets.simple_balance_view import SimpleBalanceView
from tools.date_time_tool import get_current_date, get_current_month, get_last_week
from tools.my_logger import logger
from widgets.week_balance_view import WeekBalanceView

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
        self.menu_bar = self.menuBar()
        self.set_interface_language(menu_language)
        self.make_menu()
        self.db_handler = SqlHandler(self.app_dir)
        self.check_db()
        self.set_simple_balance_view()
        self.status_bar = self.statusBar()
        self.show_current_date()


    def set_interface_language(self, language: str):
        if language == 'en':
            self.interface_language = MenuLanguages.en
        else:
            self.interface_language = MenuLanguages.ru
        settings.setValue('Language', language)

    def make_menu(self):
        my_menu_viewing = self.menu_bar.addMenu(self.interface_language['viewing'])
        my_menu_edit = self.menu_bar.addMenu(self.interface_language['edit'])
        self.make_viewing_menu(my_menu_viewing)
        self.make_edit_menu(my_menu_edit)

    def make_viewing_menu(self, viewing: QtWidgets.QMenuBar):
        viewing.addAction(self.interface_language['simple_view'], self.set_simple_balance_view)
        viewing.addAction(self.interface_language['month_view'], self.set_month_balance_view)
        viewing.addAction(self.interface_language['week'], self.set_week_balance_view)
        viewing.addAction(self.interface_language['day'], self.set_day_balance_view)
        viewing.addAction(self.interface_language['income'], self.set_month_income_view)

    def make_edit_menu(self, editing: QtWidgets.QMenuBar):
        editing.addAction(self.interface_language['edit_record'], self.change_record)


    def update_view(self):
        self.view.btn_close.clicked.connect(self.close)
        self.view.simple_balance_button.clicked.connect(lambda: self.set_simple_balance_view())
        self.view.month_balance_button.clicked.connect(lambda: self.set_month_balance_view())
        self.view.btn_submit_choose_viewing.clicked.connect(self.select_view)

    def select_view(self):
        type_viewing = self.view.get_type_viewing()
        match type_viewing:
            case 0:
                self.set_simple_balance_view()
            case 1:
                self.set_month_balance_view()
            case 2:
                self.set_week_balance_view()
            case 3:
                self.set_day_balance_view()
            case 4:
                self.set_month_income_view()

    def set_simple_balance_view(self):
        if hasattr(self, 'view') and self.view.__class__.__name__ == 'SimpleBalanceView':
            logger.info('Class: SimpleBalanceView')
        else:
            self.view = SimpleBalanceView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            current_month_date, _ = get_current_month()
            self.view.start_screen(current_month_date)
            self.update_view()

    def set_month_balance_view(self):
        if self.view.__class__.__name__ == 'MonthBalanceView':
            logger.info('Class: MonthBalanceView')
        else:
            self.view = MonthBalanceView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            current_month_date, _ = get_current_month()
            self.view.balance_screen(current_month_date)
            self.update_view()
            window.resize(475, 350)

    def set_week_balance_view(self):
        if self.view.__class__.__name__ == 'WeekBalanceView':
            logger.info('Class: WeekBalanceView')
        else:
            self.view = WeekBalanceView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            last_week = get_last_week()
            self.view.balance_screen(last_week)
            self.update_view()
            window.resize(475, 350)

    def set_day_balance_view(self):
        if self.view.__class__.__name__ == 'DayBalanceView':
            logger.info('Class: DayBalanceView')
        else:
            self.view = DayBalanceView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            current_day = get_current_date('day')
            self.view.balance_screen(current_day)
            self.update_view()
            window.resize(475, 350)

    def set_month_income_view(self):
        if self.view.__class__.__name__ == 'MonthIncomeView':
            logger.info('Class: MonthIncomeView')
        else:
            self.view = MonthIncomeView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            current_month_date, _ = get_current_month()
            self.view.balance_screen(current_month_date)
            self.update_view()
            window.resize(475, 350)

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

    def change_record(self):
        if self.view.__class__.__name__ == 'SimpleBalanceView':
            logger.info('Class: SimpleBalanceView')
        elif self.view.__class__.__name__ == 'MonthIncomeView':
            self.view.edit_record(self.view.table_view, self.view.standard_item, 'income')
        else:
            self.view.edit_record(self.view.table_view, self.view.standard_item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Mein Buchhalter")
    window.resize(360, 150)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())

