#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger

from PyQt5 import QtWidgets

from tools.data_unpacking import unpacking
from widgets.category_selected_period_view import CategorySelectedPeriodView

logger = getLogger(__name__)


class NoteCategorySelectedPeriodView(CategorySelectedPeriodView):

    def selected_note(self, category: bool):
        title = QtWidgets.QLabel(self.interface_languages['note'])
        self.view_box.addWidget(title)
        choose_note_widget = self.choose_note(category)
        self.view_box.addWidget(choose_note_widget)

    def get_data(self, start_date: str, table_names: tuple, stop_date: str):
        return unpacking(self.get_time_span_note_values(start_date, table_names, stop_date))
