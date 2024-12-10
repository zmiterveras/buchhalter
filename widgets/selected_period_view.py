#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from widgets.month_balance_view import MonthBalanceView


class SelectedPeriodView(MonthBalanceView):

    def selected_period(self):
        choose_period_widget = self.choose_time_span_widget()
        self.view_box.addWidget()