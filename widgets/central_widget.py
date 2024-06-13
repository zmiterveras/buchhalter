#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from menu_languages.menulanguages import MenuLanguages


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, interface, sql_handler, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.interface_languages = interface
        self.sql_handler = sql_handler
        self.cat_keys = MenuLanguages.cat_keys
        self.make_widget()
        self.make_buttons_box()

    def make_widget(self):
        self.top_widget = QtWidgets.QVBoxLayout()
        self.view_box = QtWidgets.QVBoxLayout()
        self.buttons_box = QtWidgets.QHBoxLayout()
        self.top_widget.addLayout(self.view_box)
        self.top_widget.addLayout(self.buttons_box)
        self.setLayout(self.top_widget)

    def clear_top_widget(self):
        self.clear_view_box()
        self.clear_buttons_box()

    def clear_view_box(self):
        for i in reversed(range(self.view_box.count())):
            widget = self.view_box.itemAt(i).widget()
            widget.setParent(None)
            widget.deleteLater()

    def clear_buttons_box(self):
        for i in reversed(range(self.buttons_box.count())):
            widget = self.buttons_box.itemAt(i).widget()
            widget.setParent(None)
            widget.deleteLater()


