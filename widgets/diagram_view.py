#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from logging import getLogger
from widgets.controller import Controller
from tools.data_unpacking import unpacking_diagram
from tools.matplotlib_canvas import MplCanvas


logger = getLogger(__name__)


class DiagramView(Controller):

    def selected_period(self):
        title = QtWidgets.QLabel(self.interface_languages['select_period_table'])
        self.view_box.addWidget(title)
        choose_period_widget = self.choose_time_span()
        self.view_box.addWidget(choose_period_widget)

    def get_data(self, start_date: str, stop_date: str, table_names: tuple):
        return unpacking_diagram(self.get_diagram_values(start_date, table_names, stop_date))

    def set_table(self,start_date: str, stop_date: str, table_names: tuple, table: str):
        cat_names, values, values_str = self.get_data(start_date, stop_date, table_names)
        mpl_canvas = MplCanvas(self, 5, 4, 100)
        # mpl_canvas.axes.plot([0,1,2,3,4], [10, 15, 5, 10, 25])
        mpl_canvas.axes.pie(values, labels=cat_names)
        # mpl_canvas.axes.pie([10, 42, 16], labels=['a', 'b', 'c'])
        self.view_box.addWidget(mpl_canvas)

