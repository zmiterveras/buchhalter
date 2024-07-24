#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui

from widgets.central_widget import CentralWidget
from tools.money_parser import get_view_money
from logging import getLogger
from tools.date_time_tool import get_current_date


logger = getLogger(__name__)


class MonthBalanceView(CentralWidget):

    def month_balance_screen(self):
        month = get_current_date('month') + ':'
        label = QtWidgets.QLabel(month.capitalize())
        self.view_box.addWidget(label)
        self.set_table_month_expense()

    def set_table_month_expense(self):
        ids, dates, values, categories = self.unpacking_month_expense(self.get_month_expense())
        total_value = get_view_money(self.get_current_expense())
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

    def unpacking_month_expense(self, month_expense):
        ids = []
        dates = []
        values = []
        categories = []
        for id_note, date, value, category in month_expense:
            ids.append(id_note)
            dates.append(date)
            values.append(get_view_money(value))
            categories.append(category)
        return ids, dates, values, categories

    def balance_update(self, current_balance: str):
        match current_balance:
            case 'credit':
                self.clear_view_box()
                self.month_balance_screen()
            case 'debit':
                pass


