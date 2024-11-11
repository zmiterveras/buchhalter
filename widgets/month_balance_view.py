#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui

from tools.data_unpacking import unpacking_expense
from widgets.central_widget import CentralWidget
from tools.money_parser import get_view_money
from logging import getLogger
from tools.date_time_tool import get_current_date, get_current_month

logger = getLogger(__name__)


class MonthBalanceView(CentralWidget):

    def balance_screen(self, date: str):
        balance = get_view_money(self.get_current_balance())
        label_month = self.set_title_label()
        self.label_balance = QtWidgets.QLabel(self.interface_languages['current_balance'] + ' ' + balance)
        self.view_box.addWidget(label_month)
        self.view_box.addWidget(self.label_balance)
        self.set_table_expense(date)

    def set_title_label(self):
        month = get_current_date('month')
        return QtWidgets.QLabel(self.interface_languages['month'] + ': ' + month)

    def set_table_expense(self, date: str):
        ids, dates, values, categories, notes = unpacking_expense(self.get_last_time_span_expense(date))
        total_value = get_view_money(self.get_current_expense(date))
        self.table_view = QtWidgets.QTableView(parent=None)
        self.standard_item = QtGui.QStandardItemModel(parent=None)
        for row in range(0, len(ids)):
            item1 = QtGui.QStandardItem(str(ids[row]))
            item2 = QtGui.QStandardItem(dates[row])
            item3 = QtGui.QStandardItem(values[row])
            item4 = QtGui.QStandardItem(categories[row])
            item5 = QtGui.QStandardItem(notes[row])
            self.standard_item.appendRow([item1, item2, item3, item4, item5])
        total_row = []
        for i in [0, self.interface_languages['sum'], str(total_value), '']:
            total_row.append(QtGui.QStandardItem(i))
        self.standard_item.appendRow(total_row)
        self.standard_item.setHorizontalHeaderLabels(['id', self.interface_languages['date'],
                                                 self.interface_languages['expense'],
                                                 self.interface_languages['category'],
                                                 self.interface_languages['note']])
        self.table_view.setModel(self.standard_item)
        self.table_view.hideColumn(0)
        self.view_box.addWidget(self.table_view)

    def balance_update(self, current_balance: str):
        match current_balance:
            case 'credit':
                current_month_date, _ = get_current_month()
                self.clear_view_box()
                self.balance_screen(current_month_date)
            case 'debit':
                balance = get_view_money(self.get_current_balance())
                self.label_balance.setText(self.interface_languages['current_balance'] + ' ' + balance)

    def get_row(self, col=5):
        row_number = self.table_view.currentIndex().row()
        row = []
        for i in range(col):
            index = self.standard_item.index(row_number, i)
            row.append(self.standard_item.data(index))
        logger.debug('Get row: ' + str(row))
        return row

    def change(self, flag='change') -> (int, list):
        match flag:
            case 'delete':
                warn_word = self.interface_languages['warn_delete']
            case _:
                warn_word = self.interface_languages['warn_change']
        row = self.get_row()
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


    def edit_record(self):
        result, row = self.change()
        if result == 16384:
            logger.debug('Get record: ' + str(row))






