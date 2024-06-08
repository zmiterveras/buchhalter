#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5 import QtSql
from tools.date_time_tool import get_current_month
from logging import getLogger


logger = getLogger(__name__)


class SqlHandler:
    def __init__(self, root_path):
        self.database = os.path.join(root_path, 'bases/buchhaltungDB.sqlite')

    def create_db(self):
        connect, query = self.connect_db()
        self.create_credit(connect, query)
        self.create_debit(connect, query)
        self.create_balance(connect, query)
        self.create_accounts(connect, query)
        self.create_category(connect, query)
        connect.close()
        logger.info('Created database')

    def create_credit(self, connect, query):
        if 'Credit' not in connect.tables():
            query_create_credit = '''
            create table Credit (id integer primary key autoincrement,
            date text, value integer, cat_id integer, note text)
            '''
            query.exec(query_create_credit)
            query.clear()

    def create_debit(self, connect, query):
        if 'Debit' not in connect.tables():
            query_create_debit = '''
            create table Debit (id integer primary key autoincrement,
            salary integer, bonus integer, gift integer, percents integer, date text, note text)
            '''
            query.exec(query_create_debit)
            query.clear()

    def create_balance(self, connect, query):
        if 'Balance' not in connect.tables():
            query_create_balance = '''
            create table Balance (id integer primary key autoincrement, balance integer)
            '''
            query.exec(query_create_balance)
            query.clear()
            self.fill_balance(query)

    def fill_balance(self, query):
        query_fill_balance = '''
        insert into Balance (null, 0)
        '''
        query.exec(query_fill_balance)
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
        query.prepare("insert into Category (null, :en_names, :ru_names)")
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

    def get_current_credit(self) -> int:
        credit_sum = 0
        connect, query = self.connect_db()
        current_month_date, _ = get_current_month()
        query_get_current_credit = '''
        select sum(value) as credit_sum from Credit where date>="%s"
        ''' % current_month_date
        query.exec(query_get_current_credit)
        if query.isActive():
            query.first()
            while query.isValid():
                credit_sum = query.value('credit_sum')
                query.next()
                logger.info('get_current_credit: ' + str(credit_sum))
        else:
            logger.error('Problem with query')
        connect.close()
        return credit_sum

    def get_current_debit(self) -> int:
        debit_sum = 0
        connect, query = self.connect_db()
        current_month_date, _ = get_current_month()
        query_get_current_debit = '''
        select sum(salary) + sum(bonus) + sum(gift) + sum(percents) as debit_sum from Debit where date>="%s"
        ''' % current_month_date
        query.exec(query_get_current_debit)
        if query.isActive():
            query.first()
            while query.isValid():
                debit_sum = query.value('debit_sum')
                query.next()
                logger.info('get_current_debit: ' + str(debit_sum))
        else:
            logger.error('Problem with query')
        connect.close()
        return debit_sum

    def add_credit(self, date, value, cat_id, note):
        connect, query = self.connect_db()
        query.prepare('insert into Credit values (null, ?, ?, ?, ?)')
        query.addBindValue(date)
        query.addBindValue(value)
        query.addBindValue(cat_id)
        query.addBindValue(note)
        query.exec_()
        query.clear()
        # self.update_balance(query, credit=value)
        connect.close()
        logger.info('Add new record to Credit')

    def add_debit(self, date, salary, bonus, gift, percent,  note):
        connect, query = self.connect_db()
        query.prepare('insert into Debit values (null, ?, ?, ?, ?, ?, ?)')
        query.addBindValue(salary)
        query.addBindValue(bonus)
        query.addBindValue(gift)
        query.addBindValue(percent)
        query.addBindValue(date)
        query.addBindValue(note)
        query.exec_()
        query.clear()
        # self.update_balance(query, debit=salary+bonus+gift+percent)
        connect.close()
        logger.info('Add new record to Debit')

    def update_balance(self, query, credit=0, debit=0):
        balance = self.get_balance()
        balance = balance + debit - credit
        self.set_balance(query, balance)

    def get_balance(self):
        balance = 0
        connect, query = self.connect_db()
        query_get_balance = '''
        select balance from Balance
        '''
        query.exec(query_get_balance)
        if query.isActive():
            query.first()
            while query.isValid():
                balance = query.value('balance')
                query.next()
                logger.info('Got Balance: ' + balance)
        else:
            logger.error('Problem with query')
        connect.close()
        return balance

    def set_balance(self, query, balance):
        query_set_balance = '''
        update Balance set balance="%d"''' % balance
        query.exec(query_set_balance)
        logger.info('Set Balance: ' + str(balance))
        query.clear()

