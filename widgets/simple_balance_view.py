#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from PyQt5 import QtWidgets, QtCore

from tools.money_parser import get_view_money
from tools.date_time_tool import get_current_month
from widgets.central_widget import CentralWidget
from logging import getLogger

from widgets.controller import Controller

logger = getLogger(__name__)


class SimpleBalanceView(Controller):

    def start_screen(self, date: str):
        self.show_current_balance()
        start_screen_widget = QtWidgets.QWidget()
        start_screen_main_box = QtWidgets.QHBoxLayout()
        start_screen_first_box = QtWidgets.QVBoxLayout()
        start_screen_second_box = QtWidgets.QVBoxLayout()
        start_screen_second_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.show_current_expense(start_screen_first_box, date)
        self.show_current_income(start_screen_second_box, date)
        start_screen_main_box.addLayout(start_screen_first_box)
        start_screen_main_box.addLayout(start_screen_second_box)
        start_screen_widget.setLayout(start_screen_main_box)
        self.view_box.addWidget(start_screen_widget)

    def show_current_expense(self, box: QtWidgets.QVBoxLayout, date: str):
        box.addWidget(QtWidgets.QLabel(self.interface_languages['expense']))
        current_expense = self.get_current_expense(date)
        self.current_expense_label = QtWidgets.QLabel(get_view_money(current_expense))
        box.addWidget(self.current_expense_label)

    def show_current_income(self, box: QtWidgets.QVBoxLayout, date: str):
        box.addWidget(QtWidgets.QLabel(self.interface_languages['income']))
        current_income = self.get_current_income(date)
        self.current_income_label = QtWidgets.QLabel(get_view_money(current_income))
        box.addWidget(self.current_income_label)

    def show_current_balance(self):
        start_screen_header = QtWidgets.QLabel(self.interface_languages['current_balance'])
        start_screen_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.view_box.addWidget(start_screen_header)
        current_balance = self.get_current_balance()
        self.current_balance_label = QtWidgets.QLabel(get_view_money(current_balance))
        self.current_balance_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.view_box.addWidget(self.current_balance_label)

    def balance_update(self, current_balance: str):
        date, _ = get_current_month()
        match current_balance:
            case 'Credit':
                credit = self.get_current_expense(date)
                self.current_expense_label.setText(get_view_money(credit))
            case 'Debit':
                debit = self.get_current_income(date)
                self.current_income_label.setText(get_view_money(debit))
        balance = self.get_current_balance()
        self.current_balance_label.setText(get_view_money(balance))



    def test(self):
        pass
