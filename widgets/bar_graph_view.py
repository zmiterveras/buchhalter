#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from logging import getLogger

from matplotlib.lines import lineStyles

from widgets.controller import Controller
from tools.data_unpacking import unpacking_diagram
from tools.matplotlib_canvas import MplCanvas


class BarGraphView(Controller):

    def set_table(self, period: bool, type_info: bool, name: str):
        time_interval = self.interface_languages['year'] if period else self.interface_languages['half_year']
        values, names = self.get_bar_graph_values(period, name)
        mpl_canvas = MplCanvas(self, 5, 4, 100)
        mpl_canvas.axes.set_title(f'{time_interval}: {names[0]} - {names[-1]}')
        mpl_canvas.axes.grid(axis="y", linestyle="--", linewidth=0.5)
        mpl_canvas.axes.set_ylabel(self.interface_languages[name])
        mpl_canvas.axes.bar(names, values)
        self.view_box.addWidget(mpl_canvas)