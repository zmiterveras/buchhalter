#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, interface, parent=None):
        super().__init__(parent)
        self.interface_languages = interface
        self.make_widget()
        self.make_buttons_box()

    def make_widget(self):
        self.top_widget = QtWidgets.QVBoxLayout()
        self.view_box = QtWidgets.QVBoxLayout()
        self.buttons_box = QtWidgets.QHBoxLayout()
        self.top_widget.addLayout(self.view_box)
        self.top_widget.addLayout(self.buttons_box)
        self.setLayout(self.top_widget)

    def start_screen(self):
        start_screen_header = QtWidgets.QLabel(self.interface_languages['current_balance'])
        start_screen_header.setAlignment(QtCore.Qt.AlignCenter)
        self.view_box.addWidget(start_screen_header)
        start_screen_widget = QtWidgets.QWidget()
        start_screen_main_box = QtWidgets.QHBoxLayout()
        start_screen_first_box = QtWidgets.QVBoxLayout()
        start_screen_second_box = QtWidgets.QVBoxLayout()
        start_screen_second_box.setAlignment(QtCore.Qt.AlignRight)
        start_screen_first_box.addWidget(QtWidgets.QLabel(self.interface_languages['expense']))
        start_screen_first_box.addWidget(QtWidgets.QLabel('0'))
        start_screen_second_box.addWidget(QtWidgets.QLabel(self.interface_languages['income']))
        start_screen_second_box.addWidget(QtWidgets.QLabel('0'))
        start_screen_main_box.addLayout(start_screen_first_box)
        start_screen_main_box.addLayout(start_screen_second_box)
        start_screen_widget.setLayout(start_screen_main_box)
        self.view_box.addWidget(start_screen_widget)

    def make_buttons_box(self):
        for name, func in ((self.interface_languages['new'], None),
                           (self.interface_languages['viewing'], None)):
            btn = QtWidgets.QPushButton(name)
            self.buttons_box.addWidget(btn)
        self.btn_close = QtWidgets.QPushButton(self.interface_languages['close'])
        self.buttons_box.addWidget(self.btn_close)

