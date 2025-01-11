#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger

from PyQt5 import QtWidgets

from tools.data_unpacking import unpacking
from widgets.month_balance_view import MonthBalanceView

logger = getLogger(__name__)


class CategorySelectedPeriodView(MonthBalanceView):

    def selected_category(self):
        title = QtWidgets.QLabel(self.interface_languages['category'])
        self.view_box.addWidget(title)
        choose_category = self.choose_category()
        self.view_box.addWidget(choose_category)

    def get_data(self, start_date: str, table_names: tuple, stop_date: str):
        return unpacking(self.get_time_span_category_values(start_date, table_names, stop_date))