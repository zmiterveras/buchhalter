#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui

from logging import getLogger

from tools.date_time_tool import get_current_month
from tools.money_parser import get_view_money
from widgets.month_balance_view import MonthBalanceView

logger = getLogger(__name__)


class MonthIncomeView(MonthBalanceView):

    def set_table(self, start_date: str, stop_date: str | None, table_names=('Debit', 'Category_Debit'), name='income'):
        super().set_table(start_date, stop_date, table_names, name)

    def balance_update(self, current_balance: str):
        match current_balance:
            case 'Credit':
                balance = get_view_money(self.get_current_balance())
                self.label_balance.setText(self.interface_languages['current_balance'] + ' ' + balance)
            case 'Debit':
                self.clear_view_box()
                current_month_date, _ = get_current_month()
                self.balance_screen(current_month_date)


