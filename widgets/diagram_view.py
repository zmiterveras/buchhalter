#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from logging import getLogger

from tools.tools import get_explode_list
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
        exp_list = get_explode_list(values)
        mpl_canvas.axes.pie(values, labels=cat_names, explode=exp_list, autopct='%1.1f%%', rotatelabels=True)
        table_name = self.interface_languages['expense'] if table_names[0] == 'Credit' \
            else self.interface_languages['income']
        title = f'{table_name} {self.interface_languages['diagram'].lower()}: {start_date} - {stop_date}'
        title_label = QtWidgets.QLabel(title)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.view_box.addWidget(title_label)
        self.view_box.addWidget(mpl_canvas)

