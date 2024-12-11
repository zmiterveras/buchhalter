#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tools.data_unpacking import unpacking
from widgets.month_balance_view import MonthBalanceView


class SelectedPeriodView(MonthBalanceView):

    def selected_period(self):
        choose_period_widget = self.choose_time_span()
        self.view_box.addWidget(choose_period_widget)

    def get_data(self, start_date: str, table_names: list, stop_date:str):
        return unpacking(self.get_span_time_values(start_date, table_names, stop_date))