#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from widgets.central_widget import CentralWidget
from logging import getLogger


logger = getLogger(__name__)


class MonthBalanceView(CentralWidget):

    def month_balance_screen(self):
        label = QtWidgets.QLabel('MonthBalanceView')
        self.view_box.addWidget(label)
