#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tools.date_time_tool import get_current_date, get_current_month, get_next_month
from tools.money_parser import get_int_dec
from widgets.central_widget import CentralWidget
from logging import getLogger
from PyQt5 import QtWidgets

logger = getLogger(__name__)


class Controller(CentralWidget):

    def get_current_balance(self) -> int:
        return self.sql_handler.get_balance()

    def get_current_expense(self, date: str) -> int:
        return self.sql_handler.get_current_value(date, 'Credit')

    def get_current_income(self, date: str) -> int:
        return self.sql_handler.get_current_value(date, 'Debit')

    def get_last_time_span_values(self, date: str, table_names: tuple, stop_date: str) -> []:
        return self.sql_handler.get_time_span_values(date, table_names, stop_date)

    def get_span_time_values(self, start_date: str, table_names: tuple, stop_date: str) -> []:
        return self.sql_handler.get_time_span_values(start_date, table_names, stop_date)

    def add_value_to_db(self, date, value, category, note, id_, table_name):
        self.validation_new_record(date, value, category, note, id_, self.old_value, table_name)
        self.old_value = 0

    def delete_value_from_db(self, id_, table_name, value):
        self.sql_handler.delete_value(id_, table_name, value)

    def get_from_record(self, record: list) -> tuple:
        id_ = int(record[0])
        val_int, val_dec = get_int_dec(record[2])
        value = val_int * 100 + val_dec
        return id_, value, val_int, val_dec

    def change(self, table_view, standard_item, col, flag) -> (int, list):
        match flag:
            case 'delete':
                warn_word = self.interface_languages['warn_delete']
            case _:
                warn_word = self.interface_languages['warn_change']
        row = self.get_row(table_view, standard_item, col)
        if None in row:
            QtWidgets.QMessageBox.warning(None, self.interface_languages['warning'],
                                          self.interface_languages['warn_select_record'])
            return 0, row
        else:
            result = QtWidgets.QMessageBox.question(None, self.interface_languages['warning'],
                                                    self.interface_languages['warn_change_text'] % warn_word,
                                                    buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    defaultButton=QtWidgets.QMessageBox.No)
            return result, row

    def check_values_date(self, received_date):
        current_date = get_current_date('day')
        if current_date < received_date:
            QtWidgets.QMessageBox.warning(None, self.interface_languages['warning'],
                                          self.interface_languages['warn_date'] + ': ' + received_date )
            return False
        return True

    def check_values_span_dates(self, start_date, stop_date):
        check_start = self.check_values_date(start_date)
        check_stop = self.check_values_date(stop_date)
        if start_date == stop_date:
            QtWidgets.QMessageBox.warning(None, self.interface_languages['warning'],
                                          self.interface_languages['warn_same_dates'])
            check_equal = False
        elif start_date > stop_date:
            QtWidgets.QMessageBox.warning(None, self.interface_languages['warning'],
                                          self.interface_languages['warn_date'])
            check_equal = False
        else:
            check_equal = True
        return check_start and check_stop and check_equal


    def validation_new_record(self, date, value: int, cat_id: int, note: str, id_: None | int,
                  old_value: int, table_name: str):
        current_date, _ = get_current_month()
        self.sql_handler.add_value(date, value, cat_id, note, id_, old_value, table_name)
        self.check_new_record_date(date, value, table_name, current_date)
        if table_name == 'Credit' and self.last_month:
            self.balance_update('Debit')
            self.last_month = False

    def check_new_record_date(self, date, value: int, table_name: str, current_date: str):
        if date < current_date:
            self.last_month = True
            logger.debug('check_new_record_date: Old Month')
            next_month = get_next_month(date)
            old_rest = self.sql_handler.get_rest(next_month)
            if old_rest:
                new_rest = old_rest[0][2] - value if table_name == 'Credit' else old_rest[0][2] + value
                self.sql_handler.add_value(next_month, new_rest, 1, old_rest[0][3], old_rest[0][0], 0,
                                           'Debit', True)
                self.check_new_record_date(next_month, value, table_name, current_date)

    def set_table_view(self,start_date: str, stop_date: str, table: str):
        table_names = ('Credit', 'Category_Credit') if table == 'Expenses' else ('Debit', 'Category_Debit')
        if self.check_values_span_dates(start_date, stop_date):
            self.clear_view_box()
            self.set_table(start_date, stop_date, table_names, table.lower()[:-1])
