#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from tools.data_unpacking import unpacking
from tools.money_parser import get_view_money
from widgets.month_balance_view import MonthBalanceView


class SelectedPeriodView(MonthBalanceView):

    def selected_period(self):
        title = QtWidgets.QLabel(self.interface_languages['select_period_table'])
        self.view_box.addWidget(title)
        choose_period_widget = self.choose_time_span()
        self.view_box.addWidget(choose_period_widget)

    def get_total_value(self, start_date: str, name: str, stop_date: str) -> str:
        return  get_view_money(self.get_span_time_total_value(start_date, 'Credit', stop_date)) \
            if name == 'expense' else get_view_money(self.get_current_income(start_date))

    def balance_update(self, current_balance: str):
        """
        this class don't use this method,
        but method is needed to avoid the crash
        """
        pass

