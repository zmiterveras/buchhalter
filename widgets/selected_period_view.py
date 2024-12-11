#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tools.data_unpacking import unpacking
from widgets.month_balance_view import MonthBalanceView


class SelectedPeriodView(MonthBalanceView):

    def selected_period(self):
        choose_period_widget = self.choose_time_span()
        self.view_box.addWidget(choose_period_widget)

