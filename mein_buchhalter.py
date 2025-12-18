#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtWidgets, QtCore
from menu_languages.menulanguages import MenuLanguages
from sql_handler.sql_handler import SqlHandler
from widgets.bar_graph_view import BarGraphView
from widgets.category_selected_period_view import CategorySelectedPeriodView
from widgets.day_balance_view import DayBalanceView
from widgets.diagram_view import DiagramView
from widgets.month_balance_view import MonthBalanceView
from widgets.month_income_view import MonthIncomeView
from widgets.note_category_selected_period import NoteCategorySelectedPeriodView
from widgets.selected_period_view import SelectedPeriodView
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
        self.date_month, _ = get_current_month()
        self.db_handler = SqlHandler(self.app_dir, self.date_month, menu_language)
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
        my_menu_settings = self.menu_bar.addMenu(self.interface_language['settings'])
        self.make_viewing_menu(my_menu_viewing)
        self.make_edit_menu(my_menu_edit)
        self.make_settings_menu(my_menu_settings)


    def make_viewing_menu(self, viewing: QtWidgets.QMenuBar):
        viewing.addAction(self.interface_language['simple_view'], self.set_simple_balance_view)
        viewing.addAction(self.interface_language['month_view'], self.set_month_balance_view)
        viewing.addAction(self.interface_language['week'], self.set_week_balance_view)
        viewing.addAction(self.interface_language['day'], self.set_day_balance_view)
        viewing.addAction(self.interface_language['income'], self.set_month_income_view)
        viewing.addAction(self.interface_language['selected_period'], self.set_selected_period)
        viewing.addAction(self.interface_language['category'], self.set_category_view)
        note = viewing.addMenu(self.interface_language['note'])
        note.addAction(self.interface_language['note_with'], self.set_note_view)
        note.addAction(self.interface_language['note_without'], lambda: self.set_note_view(False))
        graphics = viewing.addMenu(self.interface_language['graphics'])
        graphics.addAction(self.interface_language['diagram'], self.set_diagram_view)
        bar_graph = graphics.addMenu(self.interface_language['bar_graph'])
        bar_graph.addAction(f'{self.interface_language['expense']} {self.interface_language['half_year']}',
                            self.set_bar_graph_view)
        bar_graph.addAction(f'{self.interface_language['expense']} {self.interface_language['year']}',
                            lambda: self.set_bar_graph_view(True))
        bar_graph.addAction(f'{self.interface_language['income']} {self.interface_language['half_year']}',
                            lambda: self.set_bar_graph_view(name='income'))
        bar_graph.addAction(f'{self.interface_language['income']} {self.interface_language['year']}',
                            lambda: self.set_bar_graph_view(period=True, name='income'))
        bar_graph_detailed = graphics.addMenu(self.interface_language['bar_graph_detailed'])
        bar_graph_detailed.addAction(f'{self.interface_language['expense']} {self.interface_language['half_year']}',
                            lambda: self.set_bar_graph_view(type_info=True))
        bar_graph_detailed.addAction(f'{self.interface_language['expense']} {self.interface_language['year']}',
                            lambda: self.set_bar_graph_view(True, True))
        bar_graph_detailed.addAction(f'{self.interface_language['income']} {self.interface_language['half_year']}',
                            lambda: self.set_bar_graph_view(type_info=True, name='income'))
        bar_graph_detailed.addAction(f'{self.interface_language['income']} {self.interface_language['year']}',
                            lambda: self.set_bar_graph_view(True, True,'income'))


    def make_edit_menu(self, editing: QtWidgets.QMenuBar):
        editing.addAction(self.interface_language['edit_record'], self.change_record)
        editing.addAction(self.interface_language['delete_record'], lambda: self.change_record('delete'))

    def make_settings_menu(self, settings_menu: QtWidgets.QMenuBar):
        settings_menu.addSection('Menu language')
        settings_menu.addAction('english', lambda: self.change_interface_language('en'))
        settings_menu.addAction('russian', lambda: self.change_interface_language('ru'))
        settings_menu.addSeparator()

    def change_interface_language(self,  language: str):
        saved_view = self.view.__class__.__name__
        self.set_interface_language(language)
        self.menu_bar.clear()
        self.make_menu()
        self.run_selected_view(saved_view)
        self.update_view()


    def update_view(self):
        self.view.btn_close.clicked.connect(self.close)
        self.view.simple_balance_button.clicked.connect(lambda: self.set_simple_balance_view())
        self.view.month_balance_button.clicked.connect(lambda: self.set_month_balance_view())
        self.view.btn_submit_choose_viewing.clicked.connect(self.select_view)

    def select_view(self):
        type_viewing = self.view.get_type_viewing()
        self.run_selected_view(type_viewing)

    def run_selected_view(self, view: int | str):
        change_language = True if type(view) == str else False
        match view:
            case 0 | 'SimpleBalanceView':
                self.set_simple_balance_view(change_language)
            case 1 | 'MonthBalanceView':
                self.set_month_balance_view(change_language)
            case 2 | 'WeekBalanceView':
                self.set_week_balance_view(change_language)
            case 3 | 'DayBalanceView':
                self.set_day_balance_view(change_language)
            case 4 | 'MonthIncomeView':
                self.set_month_income_view(change_language)
            case 5 | 'SelectedPeriodView':
                self.set_selected_period()
            case 6 | 'CategorySelectedPeriodView':
                self.set_category_view()
            case 7 | 'NoteCategorySelectedPeriodView':
                self.set_note_view()
            case 8 | 'DiagramView':
                self.set_diagram_view()
            case 9 | 'BarGraphView':
                self.set_bar_graph_view()
            case 10 | 'BarGraphView':
                self.set_bar_graph_view(type_info=True)

    def set_simple_balance_view(self, change_language: bool = False):
        if hasattr(self, 'view') and self.view.__class__.__name__ == 'SimpleBalanceView' and not change_language:
            logger.info('Class: SimpleBalanceView')
        else:
            self.view = SimpleBalanceView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            current_month_date, _ = get_current_month()
            self.view.start_screen(current_month_date)
            self.update_view()

    def set_month_balance_view(self, change_language: bool = False):
        if self.view.__class__.__name__ == 'MonthBalanceView' and not change_language:
            logger.info('Class: MonthBalanceView')
        else:
            self.view = MonthBalanceView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            self.view.balance_screen(self.date_month)
            self.update_view()
            window.resize(475, 350)

    def set_week_balance_view(self, change_language: bool = False):
        if self.view.__class__.__name__ == 'WeekBalanceView' and not change_language:
            logger.info('Class: WeekBalanceView')
        else:
            self.view = WeekBalanceView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            last_week = get_last_week()
            self.view.balance_screen(last_week)
            self.update_view()
            window.resize(475, 350)

    def set_day_balance_view(self, change_language: bool = False):
        if self.view.__class__.__name__ == 'DayBalanceView' and not change_language:
            logger.info('Class: DayBalanceView')
        else:
            self.view = DayBalanceView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            current_day = get_current_date('day')
            self.view.balance_screen(current_day)
            self.update_view()
            window.resize(475, 350)

    def set_month_income_view(self, change_language: bool = False):
        if self.view.__class__.__name__ == 'MonthIncomeView' and not change_language:
            logger.info('Class: MonthIncomeView')
        else:
            self.view = MonthIncomeView(self.interface_language, self.db_handler)
            self.setCentralWidget(self.view)
            self.view.balance_screen(self.date_month)
            self.update_view()
            window.resize(475, 350)

    def set_selected_period(self):
        self.view = SelectedPeriodView(self.interface_language, self.db_handler)
        self.setCentralWidget(self.view)
        self.view.selected_period()
        self.update_view()
        window.resize(475, 350)

    def set_category_view(self):
        self.view = CategorySelectedPeriodView(self.interface_language, self.db_handler)
        self.setCentralWidget(self.view)
        self.view.selected_category()
        self.update_view()
        window.resize(475, 350)

    def set_note_view(self, category: bool = True):
        self.view = NoteCategorySelectedPeriodView(self.interface_language, self.db_handler)
        self.setCentralWidget(self.view)
        self.view.selected_note(category)
        self.update_view()
        window.resize(475, 350)

    def set_diagram_view(self):
        self.view = DiagramView(self.interface_language, self.db_handler)
        self.setCentralWidget(self.view)
        self.view.selected_period()
        self.update_view()
        window.resize(750, 555)

    def set_bar_graph_view(self, period: bool = False, type_info: bool = False, name: str = 'expense'):
        self.view = BarGraphView(self.interface_language, self.db_handler)
        self.setCentralWidget(self.view)
        self.view.set_table(period, type_info, name, menu_language)
        self.update_view()
        window.resize(750, 555) if not period else window.resize(1100, 555)

    def check_db(self):
        if not self.db_handler.is_db_available():
            logger.info('DB is not exist')
            self.db_handler.create_db()
        else:
            logger.info('DB is available')
            self.db_handler.check_month_rest(self.interface_language['rest'])

    def show_current_date(self):
        label_date = QtWidgets.QLabel(get_current_date())
        label_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.status_bar.addPermanentWidget(label_date)

    def change_record(self, operation: str='change'):
        if self.view.__class__.__name__ == 'SimpleBalanceView':
            logger.info('Class: SimpleBalanceView')
        elif self.view.__class__.__name__ == 'MonthIncomeView':
            self.view.edit_record(self.view.table_view, self.view.standard_item, operation, 'income')
        else:
            self.view.edit_record(self.view.table_view, self.view.standard_item, operation)


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

