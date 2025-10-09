#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger

from PyQt5 import QtWidgets

from tools.data_unpacking import unpacking
from tools.money_parser import get_view_money
from widgets.month_balance_view import MonthBalanceView

logger = getLogger(__name__)


class NoteCategorySelectedPeriodView(MonthBalanceView):

    def selected_note(self):
        title = QtWidgets.QLabel(self.interface_languages['note'])
        self.view_box.addWidget(title)
        choose_note_widget = self.choose_note()
        self.view_box.addWidget(choose_note_widget)