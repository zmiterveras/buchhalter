#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from PyQt5 import QtWidgets, QtCore
from menu_languages.menulanguages import MenuLanguages
from logging import getLogger

from sql_handler.sql_handler import SqlHandler

logger = getLogger(__name__)


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, interface: dict, sql_handler: SqlHandler, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.interface_languages = interface
        self.sql_handler = sql_handler
        self.cat_keys_credit = MenuLanguages.cat_keys_credit
        self.cat_keys_debit = MenuLanguages.cat_keys_debit
        self.make_widget()
        self.make_buttons_box()
        self.make_view_buttons_box()
        self.btn_submit_choose_viewing = QtWidgets.QPushButton(self.interface_languages['select'])
        self.old_value = 0
        self.last_month = False

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

    def make_buttons_box(self):
        for name, func in ((self.interface_languages['new_expense'], lambda: self.add_new_value('expense')),
                           (self.interface_languages['new_income'], lambda: self.add_new_value('income')),
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

    def set_calendar(self, calendar: QtWidgets.QDateEdit):
        calendar.setCalendarPopup(True)
        calendar.setDisplayFormat('yyyy.MM.dd')
        calendar.setDate(datetime.date.today())

    def add_new_value(self, flag, change=None):
        logger.info("Add New " + flag)
        self.add_new_value_widget = QtWidgets.QWidget(parent=self, flags=QtCore.Qt.Window)
        self.add_new_value_widget.setWindowTitle(self.interface_languages['new_' + flag])
        self.add_new_value_widget.setWindowModality(QtCore.Qt.WindowModal)
        self.add_new_value_widget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.calendar = QtWidgets.QDateEdit()
        self.set_calendar(self.calendar)
        self.value_int = QtWidgets.QSpinBox()
        self.value_int.setMaximum(100000)
        self.value_dec = QtWidgets.QSpinBox()
        self.value_dec.setRange(0, 99)
        self.value_dec.setWrapping(True)
        point = QtWidgets.QLabel(',')
        value_box = QtWidgets.QHBoxLayout()
        for wid in self.value_int, point, self.value_dec:
            value_box.addWidget(wid)
        self.category = QtWidgets.QComboBox()
        cat_keys = self.cat_keys_credit if flag == 'expense' else self.cat_keys_debit
        self.category.addItems([self.interface_languages[key] for key in cat_keys])
        self.note = QtWidgets.QLineEdit()
        btn_add = QtWidgets.QPushButton(self.interface_languages['add'])
        btn_close = QtWidgets.QPushButton(self.interface_languages['close'])
        button_box = QtWidgets.QHBoxLayout()
        button_box.addWidget(btn_add)
        button_box.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        if change:
            self.add_new_value_widget.setWindowTitle(self.interface_languages['change_' + flag])
            id_, self.old_value, val_int, val_dec = self.get_from_record(change)
            self.fill_widgets([(self.note,), (self.value_int, self.value_dec), (self.category,),
                               self.calendar],
                              [(change[4],), (val_int, val_dec), (change[3],), change[1]])
        else:
            id_ = None
        for name, field in ((self.interface_languages['date'], self.calendar),
                            (self.interface_languages[flag], value_box),
                            (self.interface_languages['category'], self.category),
                            (self.interface_languages['note'], self.note)):
            form.addRow(name, field)
        form.addRow(button_box)
        btn_add.clicked.connect(lambda: self.get_value(id_, flag))
        btn_close.clicked.connect(self.add_new_value_widget.close)
        self.add_new_value_widget.setLayout(form)
        self.add_new_value_widget.show()

    def get_value(self, id_, flag):
        logger.debug('Get value id: ' + str(id_))
        date = self.calendar.text()
        value = self.value_int.value() * 100 + self.value_dec.value()
        category = self.category.currentIndex() + 1
        note = self.note.text()
        if self.check_values_date(date):
            logger.info(flag + ': ' + date + '/' + str(value) + '/' + str(category) + '/' + note)
            table_name = 'Credit' if flag == 'expense' else 'Debit'
            self.add_value_to_db(date, value, category, note, id_, table_name)
            self.add_new_value_widget.close()
            self.balance_update(table_name)

    def delete_value(self, flag, change):
        id_, value, _, _ = self.get_from_record(change)
        table_name = 'Credit' if flag == 'expense' else 'Debit'
        self.delete_value_from_db(id_, table_name, value)
        self.balance_update(table_name)

    def choose_viewing(self):
        self.choose_viewing_widget = QtWidgets.QWidget(parent=self, flags=QtCore.Qt.Window)
        viewing_list = [self.interface_languages['simple_view'],
                        self.interface_languages['month_view'],
                        self.interface_languages['week'],
                        self.interface_languages['day'],
                        self.interface_languages['income']]
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

    def choose_time_span(self):
        self.choose_time_span_widget = QtWidgets.QWidget()
        self.table_cb = QtWidgets.QComboBox()
        self.table_cb.addItems([self.interface_languages['expense'], self.interface_languages['income']])
        self.calendar_start = QtWidgets.QDateEdit()
        self.calendar_stop = QtWidgets.QDateEdit()
        self.set_calendar(self.calendar_start)
        self.set_calendar(self.calendar_stop)
        form = QtWidgets.QFormLayout()
        btn_choose = QtWidgets.QPushButton(self.interface_languages['choose'])
        for name, widget in ((self.interface_languages['start_date'], self.calendar_start),
                            (self.interface_languages['stop_date'], self.calendar_stop)):
            form.addRow(name, widget)

    def get_times(self):
        table_choose = self.table_cb.currentText()
        table_name = 'Credit' if table_choose == 'expense' else 'Debit'
        start_date = self.calendar_start.text()
        stop_date = self.calendar_stop.text()
        logger.info('Start date: ' + start_date)
        logger.info('Stop date: ' + stop_date)
        self.choose_time_span_widget.close()


    def get_row(self, table_view, standard_item, col):
        row_number = table_view.currentIndex().row()
        row = []
        for i in range(col):
            index = standard_item.index(row_number, i)
            row.append(standard_item.data(index))
        logger.debug('Get row: ' + str(row))
        return row

    def test(self):
        logger.info('Test')


