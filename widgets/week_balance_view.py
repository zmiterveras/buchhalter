#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from logging import getLogger

from tools.date_time_tool import get_current_date, get_last_week
from widgets.month_balance_view import MonthBalanceView

logger = getLogger(__name__)


class WeekBalanceView(MonthBalanceView):

    def set_title_label(self):
        current_date = get_current_date()
        last_week_date = get_last_week('view')
        return QtWidgets.QLabel(self.interface_languages['week'] + ': ' +
                                last_week_date + ' - ' + current_date)
