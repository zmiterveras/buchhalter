#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from logging import getLogger

from matplotlib.lines import lineStyles

from widgets.controller import Controller
from tools.data_unpacking import unpacking_diagram
from tools.matplotlib_canvas import MplCanvas


class BarGraphView(Controller):

    def set_table(self, period: bool, type_info: bool, name: str, language: str):
        time_interval = self.interface_languages['year'] if period else self.interface_languages['half_year']
        mpl_canvas = MplCanvas(self, 5, 4, 100)
        mpl_canvas.axes.grid(axis="y", linestyle="--", linewidth=0.5)
        mpl_canvas.axes.set_xlabel(self.interface_languages['year_month'])
        mpl_canvas.axes.set_ylabel(self.interface_languages[name])
        if type_info:
            names, cat_values = self.get_data(period, name, type_info, language)
            bar_container = self.run_bar_full(mpl_canvas, names, cat_values)
        else:
            values, names = self.get_data(period, name, type_info, language)
            bar_container = self.run_bar_brief(mpl_canvas, names, values)
        mpl_canvas.axes.set_title(f'{time_interval}: {names[0]} - {names[-1]}')
        mpl_canvas.axes.bar_label(bar_container, fmt='{:.2f}')
        self.view_box.addWidget(mpl_canvas)

    def run_bar_brief(self, mpl_canvas: MplCanvas, names: list, values: list):
        return mpl_canvas.axes.bar(names, values)

    def run_bar_full(self, mpl_canvas: MplCanvas, names: list, cat_values: dict):
        bar_container = None
        bottom = [0] * len(names)
        for cat_name, values in cat_values.items():
            bar_container = mpl_canvas.axes.bar(names, values, label=cat_name, bottom=bottom)
            bottom += values
        mpl_canvas.axes.legend(loc='upper right')
        return bar_container

    def get_data(self, period: bool, name: str, type_info: bool, language: str):
        if not type_info:
            return self.get_bar_graph_values(period, name)
        else:
            return self.get_bar_graph_values_detailed(period, name, language)