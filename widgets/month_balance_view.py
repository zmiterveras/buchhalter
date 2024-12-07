#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui

from tools.data_unpacking import unpacking
from widgets.central_widget import CentralWidget
from tools.money_parser import get_view_money
from logging import getLogger
from tools.date_time_tool import get_current_date, get_current_month
from widgets.controller import Controller

logger = getLogger(__name__)


class MonthBalanceView(Controller):

    def balance_screen(self, date: str):
        balance = get_view_money(self.get_current_balance())
        label_month = self.set_title_label()
        self.label_balance = QtWidgets.QLabel(self.interface_languages['current_balance'] + ' ' + balance)
        self.view_box.addWidget(label_month)
        self.view_box.addWidget(self.label_balance)
        self.set_table(date)

    def set_title_label(self):
        month = get_current_date('month')
        return QtWidgets.QLabel(self.interface_languages['month'] + ': ' + month)

    def set_table(self, date: str, table_names=['Credit', 'Category_Credit'], name='expense'):
        ids, dates, values, categories, notes = unpacking(self.get_last_time_span_values(date, table_names))
        total_value = get_view_money(self.get_current_expense(date)) \
            if name == 'expense' else get_view_money(self.get_current_income(date))
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
                                                 self.interface_languages[name],
                                                 self.interface_languages['category'],
                                                 self.interface_languages['note']])
        self.table_view.setModel(self.standard_item)
        self.table_view.hideColumn(0)
        self.view_box.addWidget(self.table_view)

    def balance_update(self, current_balance: str):
        match current_balance:
            case 'Credit':
                self.clear_view_box()
                current_month_date, _ = get_current_month()
                self.balance_screen(current_month_date)
            case 'Debit':
                balance = get_view_money(self.get_current_balance())
                self.label_balance.setText(self.interface_languages['current_balance'] + ' ' + balance)


    def edit_record(self, table_view, standard_item, operation, flag='expense', col=5):
        result, row = self.change(table_view, standard_item, col, operation)
        if result == 16384:
            logger.debug('Get record: ' + str(row))
            if operation == 'change':
                self.add_new_value(flag, change=row)
            else:
                logger.debug('Delete record: ' + str(row))
                self.delete_value(flag, row)






