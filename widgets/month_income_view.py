#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui

from logging import getLogger

from tools.date_time_tool import get_current_date
from widgets.central_widget import CentralWidget

logger = getLogger(__name__)


class MonthIncomeView(CentralWidget):

    def incoming_screen(self):
        month = get_current_date('month')
        self.view_box.addWidget(QtWidgets.QLabel(self.interface_languages['month'] + ': ' + month))

    def set_table_income(self, date: str):
        pass