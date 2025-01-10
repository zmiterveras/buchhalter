#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger

from PyQt5 import QtWidgets

from widgets.month_balance_view import MonthBalanceView

logger = getLogger(__name__)


class CategorySelectedPeriodView(MonthBalanceView):

    def selected_category(self):
        title = QtWidgets.QLabel(self.interface_languages['category'])
        self.view_box.addWidget(title)
        choose_category = self.choose_category()
        self.view_box.addWidget(choose_category)