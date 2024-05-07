#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5 import QtSql


class SqlHandler:
    def __init__(self, root_path):
        self.database = os.path.join(root_path, 'bases/buchhaltungDB.sqlite')

    def create_db(self):
        connect, query = self.connect_db()
        self.create_credit(connect, query)
        self.create_debit(connect, query)
        self.create_accounts(connect, query)
        self.create_category(connect, query)
        connect.close()

    def create_credit(self, connect, query):
        if 'Credit' not in connect.tables():
            query_create_credit = '''
            create table Credit (id integer primary key autoincrement,
            data text, value integer, cat_id integer, note text)
            '''
            query.exec(query_create_credit)
            query.clear()

    def create_debit(self, connect, query):
        if 'Debit' not in connect.tables():
            query_create_debit = '''
            create table Debit (id integer primary key autoincrement,
            salary integer, gift integer, bonus integer, percents integer, note text)
            '''
            query.exec(query_create_debit)
            query.clear()

    def create_accounts(self, connect, query):
        if 'Accounts' not in connect.tables():
            query_create_accounts = '''
            create table Accounts (id integer primary key autoincrement,
            value integer, currency text)
            '''
            query.exec(query_create_accounts)
            query.clear()

    def create_category(self, connect, query):
        if 'Category' not in connect.tables():
            query_create_category = '''
            create table Category (id integer, category_en text, category_ru text)
            '''
            query.exec(query_create_category)
            query.clear()
            self.fill_category(query)

    def get_category_names(self):
        from menu_languages.menulanguages import MenuLanguages
        en_dict = MenuLanguages.en
        self.en_names = [en_dict[name] for name in MenuLanguages.cat_keys]
        ru_dict = MenuLanguages.ru
        self.ru_names = [ru_dict[name] for name in MenuLanguages.cat_keys]

    def fill_category(self, query):
        self.get_category_names()
        query.prepare("insert into category (null, :en_names, :ru_names)")
        query.bindValue(':en_names', self.en_names)
        query.bindValue(':ru_names', self.ru_names)
        query.execBatch()
        query.clear()

    def connect_db(self):
        connect = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        connect.setDatabaseName(self.database)
        connect.open()
        query = QtSql.QSqlQuery()
        return connect, query

    def is_db_available(self):
        return True if os.path.exists(self.database) else False


