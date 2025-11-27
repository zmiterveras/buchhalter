#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from logging import getLogger
from widgets.controller import Controller
from tools.data_unpacking import unpacking_diagram
from tools.matplotlib_canvas import MplCanvas


class BarGraphView(Controller):

    def set_table(self, period: bool = False, type_info: bool = False, name: str = 'expense'):
        values, names = self.get_bar_graph_values(period, name)
        mpl_canvas = MplCanvas(self, 5, 4, 100)
        mpl_canvas.axes.bar(names, values)
        self.view_box.addWidget(mpl_canvas)