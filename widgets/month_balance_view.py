#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui

from tools.data_unpacking import unpacking_expense
from widgets.central_widget import CentralWidget
from tools.money_parser import get_view_money
from logging import getLogger
from tools.date_time_tool import get_current_date

logger = getLogger(__name__)


class MonthBalanceView(CentralWidget):

    def balance_screen(self, date):
        balance = get_view_money(self.get_current_balance())
        label_month = self.set_title_label()
        self.label_balance = QtWidgets.QLabel(self.interface_languages['current_balance'] + ' ' + balance)
        self.view_box.addWidget(label_month)
        self.view_box.addWidget(self.label_balance)
        self.set_table_expense(date)

    def set_title_label(self):
        month = get_current_date('month')
        return QtWidgets.QLabel(self.interface_languages['month_view'] + ': ' + month)

    def set_table_expense(self, date):
        ids, dates, values, categories = unpacking_expense(self.get_last_time_span_expense(date))
        total_value = get_view_money(self.get_current_expense(date))
        table_view = QtWidgets.QTableView(parent=None)
        standard_item = QtGui.QStandardItemModel(parent=None)
        for row in range(0, len(ids)):
            item1 = QtGui.QStandardItem(str(ids[row]))
            item2 = QtGui.QStandardItem(dates[row])
            item3 = QtGui.QStandardItem(values[row])
            item4 = QtGui.QStandardItem(categories[row])
            standard_item.appendRow([item1, item2, item3, item4])
        total_row = []
        for i in [0, self.interface_languages['sum'], str(total_value), '']:
            total_row.append(QtGui.QStandardItem(i))
        standard_item.appendRow(total_row)
        standard_item.setHorizontalHeaderLabels(['id', self.interface_languages['date'],
                                                 self.interface_languages['expense'],
                                                 self.interface_languages['category']])
        table_view.setModel(standard_item)
        table_view.hideColumn(0)
        self.view_box.addWidget(table_view)

    def balance_update(self, current_balance: str):
        match current_balance:
            case 'credit':
                self.clear_view_box()
                self.balance_screen()
            case 'debit':
                balance = get_view_money(self.get_current_balance())
                self.label_balance.setText(self.interface_languages['current_balance'] + ' ' + balance)



