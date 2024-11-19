#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui

from logging import getLogger

from tools.data_unpacking import unpacking_income
from tools.date_time_tool import get_current_date
from widgets.central_widget import CentralWidget

logger = getLogger(__name__)


class MonthIncomeView(CentralWidget):

    def incoming_screen(self, date: str):
        month = get_current_date('month')
        self.view_box.addWidget(QtWidgets.QLabel(self.interface_languages['month'] + ': ' + month))
        self.set_table_income(date)

    def set_table_income(self, date: str):
        ids, salaries, bonuses, gifts, percents, dates, notes = unpacking_income(self.get_last_time_span_income(date))
        self.table_view = QtWidgets.QTableView(parent=None)
        self.standard_item = QtGui.QStandardItemModel(parent=None)
        for row in range(0, len(ids)):
            item1 = QtGui.QStandardItem(str(ids[row]))
            item2 = QtGui.QStandardItem(dates[row])
            item3 = QtGui.QStandardItem(salaries[row])
            item4 = QtGui.QStandardItem(bonuses[row])
            item5 = QtGui.QStandardItem(gifts[row])
            item6 = QtGui.QStandardItem(percents[row])
            item7 = QtGui.QStandardItem(notes[row])
            self.standard_item.appendRow([item1, item2, item3, item4, item5, item6, item7])
        self.standard_item.setHorizontalHeaderLabels(['id', self.interface_languages['date'],
                                                      self.interface_languages['salary'],
                                                      self.interface_languages['bonus'],
                                                      self.interface_languages['gift'],
                                                      self.interface_languages['percent'],
                                                      self.interface_languages['note']])
        self.table_view.setModel(self.standard_item)
        self.table_view.hideColumn(0)
        self.view_box.addWidget(self.table_view)
