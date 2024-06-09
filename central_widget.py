#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from PyQt5 import QtWidgets, QtCore
from tools.date_time_tool import get_current_date
from tools.money_parser import get_view_money
from menu_languages.menulanguages import MenuLanguages
from logging import getLogger

logger = getLogger(__name__)


def test_button():
    print('Button clicked')


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, interface, sql_handler, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.interface_languages = interface
        self.sql_handler = sql_handler
        self.cat_keys = MenuLanguages.cat_keys
        self.make_widget()
        self.make_buttons_box()

    def make_widget(self):
        self.top_widget = QtWidgets.QVBoxLayout()
        self.view_box = QtWidgets.QVBoxLayout()
        self.buttons_box = QtWidgets.QHBoxLayout()
        self.top_widget.addLayout(self.view_box)
        self.top_widget.addLayout(self.buttons_box)
        self.setLayout(self.top_widget)

    def start_screen(self):
        self.show_current_balance()
        start_screen_widget = QtWidgets.QWidget()
        start_screen_main_box = QtWidgets.QHBoxLayout()
        start_screen_first_box = QtWidgets.QVBoxLayout()
        start_screen_second_box = QtWidgets.QVBoxLayout()
        start_screen_second_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.show_current_expense(start_screen_first_box)
        self.show_current_income(start_screen_second_box)
        start_screen_main_box.addLayout(start_screen_first_box)
        start_screen_main_box.addLayout(start_screen_second_box)
        start_screen_widget.setLayout(start_screen_main_box)
        self.view_box.addWidget(start_screen_widget)

    def show_current_expense(self, box):
        box.addWidget(QtWidgets.QLabel(self.interface_languages['expense']))
        current_expense = self.sql_handler.get_current_credit()
        box.addWidget(QtWidgets.QLabel(get_view_money(current_expense)))

    def show_current_income(self, box):
        box.addWidget(QtWidgets.QLabel(self.interface_languages['income']))
        current_income = self.sql_handler.get_current_debit()
        box.addWidget(QtWidgets.QLabel(get_view_money(current_income)))

    def show_current_balance(self):
        start_screen_header = QtWidgets.QLabel(self.interface_languages['current_balance'])
        start_screen_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.view_box.addWidget(start_screen_header)
        current_balance = self.sql_handler.get_balance()
        start_screen_header_value = QtWidgets.QLabel(get_view_money(current_balance))
        start_screen_header_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.view_box.addWidget(start_screen_header_value)

    def make_buttons_box(self):
        for name, func in ((self.interface_languages['new_expense'], self.add_new_expense),
                           (self.interface_languages['new_income'], self.add_new_income),
                           (self.interface_languages['viewing'], self.test)):
            btn = QtWidgets.QPushButton(name)
            btn.clicked.connect(func)
            self.buttons_box.addWidget(btn)
        self.btn_close = QtWidgets.QPushButton(self.interface_languages['close'])
        self.buttons_box.addWidget(self.btn_close)

    def add_new_expense(self):
        logger.info("Add New Expense")
        self.add_new_expense_widget = QtWidgets.QWidget(parent=self, flags=QtCore.Qt.Window)
        self.add_new_expense_widget.setWindowTitle(self.interface_languages['new_expense'])
        self.add_new_expense_widget.setWindowModality(QtCore.Qt.WindowModal)
        self.add_new_expense_widget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.calendar = QtWidgets.QDateEdit()
        self.calendar.setCalendarPopup(True)
        self.calendar.setDisplayFormat('yyyy.MM.dd')
        self.calendar.setDate(datetime.date.today())
        self.expense_int = QtWidgets.QSpinBox()
        self.expense_int.setMaximum(100000)
        self.expense_dec = QtWidgets.QSpinBox()
        self.expense_dec.setRange(0, 99)
        point = QtWidgets.QLabel(',')
        expense_box = QtWidgets.QHBoxLayout()
        for wid in self.expense_int, point, self.expense_dec:
            expense_box.addWidget(wid)
        self.category = QtWidgets.QComboBox()
        self.category.addItems([self.interface_languages[key] for key in self.cat_keys])
        self.note = QtWidgets.QLineEdit()
        btn_add = QtWidgets.QPushButton(self.interface_languages['add'])
        btn_close = QtWidgets.QPushButton(self.interface_languages['close'])
        button_box = QtWidgets.QHBoxLayout()
        button_box.addWidget(btn_add)
        button_box.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        for name, field in ((self.interface_languages['date'], self.calendar),
                            (self.interface_languages['expense'], expense_box),
                            (self.interface_languages['category'], self.category),
                            (self.interface_languages['note'], self.note)):
            form.addRow(name, field)
        form.addRow(button_box)
        btn_add.clicked.connect(self.get_expense)
        btn_close.clicked.connect(self.add_new_expense_widget.close)
        self.add_new_expense_widget.setLayout(form)
        self.add_new_expense_widget.show()

    def add_new_income(self):
        logger.info("Add New Income")
        self.add_new_income_widget = QtWidgets.QWidget(parent=self, flags=QtCore.Qt.Window)
        self.add_new_income_widget.setWindowTitle(self.interface_languages['new_income'])
        self.add_new_income_widget.setWindowModality(QtCore.Qt.WindowModal)
        self.add_new_income_widget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.calendar_in = QtWidgets.QDateEdit()
        self.calendar_in.setCalendarPopup(True)
        self.calendar_in.setDisplayFormat('yyyy.MM.dd')
        self.calendar_in.setDate(datetime.date.today())
        ############################################################################
        self.income_dic = {}
        for name in ('salary', 'bonus', 'gift', 'percent'):
            box = QtWidgets.QHBoxLayout()
            int_value = QtWidgets.QSpinBox()
            int_value.setMaximum(100000)
            dec_value = QtWidgets.QSpinBox()
            dec_value.setRange(0, 99)
            point = QtWidgets.QLabel(',')
            for wid in int_value, point, dec_value:
                box.addWidget(wid)
            self.income_dic[name] = (box, int_value, dec_value)
        self.note_in = QtWidgets.QLineEdit()
        btn_add = QtWidgets.QPushButton(self.interface_languages['add'])
        btn_close = QtWidgets.QPushButton(self.interface_languages['close'])
        button_box = QtWidgets.QHBoxLayout()
        button_box.addWidget(btn_add)
        button_box.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        for name, field in ((self.interface_languages['date'], self.calendar_in),
                            (self.interface_languages['salary'], self.income_dic['salary'][0]),
                            (self.interface_languages['bonus'], self.income_dic['bonus'][0]),
                            (self.interface_languages['gift'], self.income_dic['gift'][0]),
                            (self.interface_languages['percent'], self.income_dic['percent'][0]),
                            (self.interface_languages['note'], self.note_in)):
            form.addRow(name, field)
        form.addRow(button_box)
        btn_add.clicked.connect(self.get_income)
        btn_close.clicked.connect(self.add_new_income_widget.close)
        self.add_new_income_widget.setLayout(form)
        self.add_new_income_widget.show()

    def get_expense(self):
        date = self.calendar.text()
        expense = self.expense_int.value() * 100 + self.expense_dec.value()
        category = self.category.currentIndex()
        note = self.note.text()
        logger.info(date + '/' + str(expense) + '/' + str(category) + '/' + note)
        self.add_expense_to_db(date, expense, category, note)
        self.add_new_expense_widget.close()

    def add_expense_to_db(self, date, value, category, note):
        self.sql_handler.add_credit(date, value, category, note)

    def get_income(self):
        date = self.calendar_in.text()
        salary = self.income_dic['salary'][1].value() * 100 + self.income_dic['salary'][2].value()
        bonus = self.income_dic['bonus'][1].value() * 100 + self.income_dic['bonus'][2].value()
        gift = self.income_dic['gift'][1].value() * 100 + self.income_dic['gift'][2].value()
        percent = self.income_dic['percent'][1].value() * 100 + self.income_dic['percent'][2].value()
        note = self.note_in.text()
        logger.info(date + '/' + str(salary) + '/' + str(bonus) + '/' + str(gift) + '/' + str(percent) + '/' + note)
        self.add_income_to_db(date, salary, bonus, gift, percent, note)
        self.add_new_income_widget.close()

    def add_income_to_db(self, date, salary, bonus, gift, percent, note):
        self.sql_handler.add_debit(date, salary, bonus, gift, percent, note)

    def test(self):
        pass
