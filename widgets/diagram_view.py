#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from logging import getLogger
from widgets.controller import Controller


logger = getLogger(__name__)


class DiagramView(Controller):

    def selected_period(self):
        title = QtWidgets.QLabel(self.interface_languages['select_period_table'])
        self.view_box.addWidget(title)
        choose_period_widget = self.choose_time_span()
        self.view_box.addWidget(choose_period_widget)

    def set_table(self,start_date: str, stop_date: str, table_names: tuple, table: str):
        pass
