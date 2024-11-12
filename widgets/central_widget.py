#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from PyQt5 import QtWidgets, QtCore
from menu_languages.menulanguages import MenuLanguages
from logging import getLogger

from sql_handler.sql_handler import SqlHandler
from tools.money_parser import get_int_dec

logger = getLogger(__name__)


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, interface: dict, sql_handler: SqlHandler, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.interface_languages = interface
        self.sql_handler = sql_handler
        self.cat_keys = MenuLanguages.cat_keys
        self.make_widget()
        self.make_buttons_box()
        self.make_view_buttons_box()
        self.btn_submit_choose_viewing = QtWidgets.QPushButton(self.interface_languages['select'])

    def make_widget(self):
        self.top_widget = QtWidgets.QVBoxLayout()
        self.view_box = QtWidgets.QVBoxLayout()
        self.buttons_box = QtWidgets.QHBoxLayout()
        self.view_buttons_box = QtWidgets.QHBoxLayout()
        self.top_widget.addLayout(self.view_box)
        self.top_widget.addLayout(self.buttons_box)
        self.top_widget.addLayout(self.view_buttons_box)
        self.setLayout(self.top_widget)

    def clear_top_widget(self):
        self.clear_view_box()
        self.clear_buttons_box()

    def clear_view_box(self):
        for i in reversed(range(self.view_box.count())):
            widget = self.view_box.itemAt(i).widget()
            widget.setParent(None)
            widget.deleteLater()

    def clear_buttons_box(self):
        for i in reversed(range(self.buttons_box.count())):
            widget = self.buttons_box.itemAt(i).widget()
            widget.setParent(None)
            widget.deleteLater()

    def get_current_balance(self) -> int:
        return self.sql_handler.get_balance()

    def get_current_expense(self, date: str) -> int:
        return self.sql_handler.get_current_credit(date)

    def get_current_income(self) -> int:
        return self.sql_handler.get_current_debit()

    def get_last_time_span_expense(self, date: str) -> []:
        return self.sql_handler.get_last_time_span_credits(date)

    def make_buttons_box(self):
        for name, func in ((self.interface_languages['new_expense'], self.add_new_expense),
                           (self.interface_languages['new_income'], self.add_new_income),
                           (self.interface_languages['viewing'], self.choose_viewing)):
            btn = QtWidgets.QPushButton(name)
            btn.clicked.connect(func)
            self.buttons_box.addWidget(btn)

    def make_view_buttons_box(self):
        self.simple_balance_button = QtWidgets.QPushButton(self.interface_languages['simple_view'])
        self.month_balance_button = QtWidgets.QPushButton(self.interface_languages['month_view'])
        self.btn_close = QtWidgets.QPushButton(self.interface_languages['close'])
        for i in (self.simple_balance_button,
                  self.month_balance_button,
                  self.btn_close):
            self.view_buttons_box.addWidget(i)

    def fill_widgets(self, widgets: list, values: list):
        """
        :param widgets: text widgets, spinbox widgets, combobox widgets, data widget
        :param values: text, int, data
        :return:
        """
        for w, v in zip(widgets[0], values[0]):
            w.setText(v)
        for w, v in zip(widgets[1], values[1]):
            w.setValue(v)
        for w, v in zip(widgets[2], values[2]):
            w.setCurrentText(v)
        date_list = values[3].split('.')
        widgets[3].setDate(QtCore.QDate(int(date_list[0]), int(date_list[1]), int(date_list[2])))


    def add_new_expense(self, change=None):
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
        if change:
            self.add_new_expense_widget.setWindowTitle(self.interface_languages['change_expense'])
            val_int, val_dec = get_int_dec(change[2])
            self.fill_widgets([(self.note,), (self.expense_int, self.expense_dec), (self.category,),
                               self.calendar],
                              [(change[4],), (val_int, val_dec), (change[3],), change[1]])
            id_ = int(change[0])
        else:
            id_ = None
        for name, field in ((self.interface_languages['date'], self.calendar),
                            (self.interface_languages['expense'], expense_box),
                            (self.interface_languages['category'], self.category),
                            (self.interface_languages['note'], self.note)):
            form.addRow(name, field)
        form.addRow(button_box)
        btn_add.clicked.connect(lambda: self.get_expense(id_))
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

    def get_expense(self, id_):
        logger.debug('Get expense id: ' + str(id_))
        date = self.calendar.text()
        expense = self.expense_int.value() * 100 + self.expense_dec.value()
        category = self.category.currentIndex() + 1
        note = self.note.text()
        logger.info('credit: ' + date + '/' + str(expense) + '/' + str(category) + '/' + note)
        self.add_expense_to_db(date, expense, category, note, id_)
        self.add_new_expense_widget.close()
        self.balance_update('credit')

    def add_expense_to_db(self, date, value, category, note, id_):
        self.sql_handler.add_credit(date, value, category, note, id_)

    def get_income(self):
        date = self.calendar_in.text()
        salary = self.income_dic['salary'][1].value() * 100 + self.income_dic['salary'][2].value()
        bonus = self.income_dic['bonus'][1].value() * 100 + self.income_dic['bonus'][2].value()
        gift = self.income_dic['gift'][1].value() * 100 + self.income_dic['gift'][2].value()
        percent = self.income_dic['percent'][1].value() * 100 + self.income_dic['percent'][2].value()
        note = self.note_in.text()
        logger.info('debit' + date + '/' + str(salary) + '/' + str(bonus) + '/' + str(gift) + '/' + str(percent)
                    + '/' + note)
        self.add_income_to_db(date, salary, bonus, gift, percent, note)
        self.add_new_income_widget.close()
        self.balance_update('debit')

    def add_income_to_db(self, date: str, salary: int, bonus: int, gift: int, percent: int, note: str):
        self.sql_handler.add_debit(date, salary, bonus, gift, percent, note)

    def choose_viewing(self):
        self.choose_viewing_widget = QtWidgets.QWidget(parent=self, flags=QtCore.Qt.Window)
        viewing_list = [self.interface_languages['simple_view'],
                        self.interface_languages['month_view'],
                        self.interface_languages['week'],
                        self.interface_languages['day']]
        choose_viewing_box = QtWidgets.QVBoxLayout()
        self.cb_viewing = QtWidgets.QComboBox()
        self.cb_viewing.addItems(viewing_list)
        choose_viewing_box.addWidget(self.cb_viewing)
        choose_viewing_box.addWidget(self.btn_submit_choose_viewing)
        self.choose_viewing_widget.setLayout(choose_viewing_box)
        self.choose_viewing_widget.show()

    def get_type_viewing(self) -> int:
        type_viewing = self.cb_viewing.currentIndex()
        self.choose_viewing_widget.close()
        return type_viewing

    def test(self):
        logger.info('Test')


