#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5 import QtSql


class SqlHandler:
    def __init__(self, root_path):
        self.database = os.path.join(root_path, 'bases/buchhaltungDB.sqlite')

    def create_db(self):
        connect, query = self.connect_db()
        if 'Credit' not in connect.tables():
            query_create_credit = '''
            create table Credit (id integer primary key autoincrement,
            data text, value integer, cat_id integer, note text)
            '''
            query.exec(query_create_credit)
            query.clear()
        if 'Debit' not in connect.tables():
            query_create_debit = '''
            create table Debit (id integer primary key autoincrement,
            salary integer, gift integer, bonus integer, percents integer, note text)
            '''
            query.exec(query_create_debit)
            query.clear()
        if 'Accounts' not in connect.tables():
            query_create_accounts = '''
            create table Accounts (id integer primary key autoincrement,
            value integer, currency text)
            '''
            query.exec(query_create_accounts)
            query.clear()
        if 'Category' not in connect.tables():
            query_create_category = '''
            create table Category (id integer, category text)
            '''
            query.exec(query_create_category)
            query.clear()
        connect.close()

    def connect_db(self):
        connect = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        connect.setDatabaseName(self.database)
        connect.open()
        query = QtSql.QSqlQuery()
        return connect, query

    def is_db_available(self):
        return True if os.path.exists(self.database) else False


