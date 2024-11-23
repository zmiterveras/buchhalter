#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui

from logging import getLogger

from widgets.month_balance_view import MonthBalanceView

logger = getLogger(__name__)


class MonthIncomeView(MonthBalanceView):

    def set_table(self, date: str, table_names=['Debit', 'Category_Debit'], name='income'):
        super().set_table(date, table_names, name)


