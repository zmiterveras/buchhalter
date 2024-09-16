#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from logging import getLogger

from tools.date_time_tool import get_current_date
from widgets.month_balance_view import MonthBalanceView

logger = getLogger(__name__)


class DayBalanceView(MonthBalanceView):

    def set_title_label(self):
        current_date = get_current_date()
        return QtWidgets.QLabel(self.interface_languages['day'] + ': ' + current_date)