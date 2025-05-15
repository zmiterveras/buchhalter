#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List, Tuple, Any

from PyQt5 import QtSql
from logging import getLogger


logger = getLogger(__name__)


class SqlHandler:
    def __init__(self, root_path: str, date, language: str):
        self.database = os.path.join(root_path, 'bases/buchhaltungDB.sqlite')
        self.date = date
        self.set_category_language(language)

    def set_category_language(self, language):
        match language:
            case 'en':
                self.category_language = 'category_en'
            case 'ru':
                self.category_language = 'category_ru'

    def create_db(self):
        connect, query = self.connect_db()
        self.create_table(connect, query, 'Credit')
        self.create_table(connect, query, 'Debit')
        self.create_balance(connect, query, self.date)
        self.create_accounts(connect, query)
        self.create_category(connect, query, 'Category_Credit')
        self.create_category(connect, query, 'Category_Debit')
        connect.close()
        logger.info('Created database')

    def create_table(self, connect, query, name):
        if name not in connect.tables():
            query_create_credit = '''
            create table %s (id integer primary key autoincrement,
            date text, value integer, cat_id integer, note text)
            ''' % name
            query.exec(query_create_credit)
            query.clear()

    def create_balance(self, connect, query, date):
        if 'Balance' not in connect.tables():
            query_create_balance = '''
            create table Balance (id integer primary key autoincrement, balance integer, date text)
            '''
            query.exec(query_create_balance)
            query.clear()
            self.fill_balance(query, date)

    def fill_balance(self, query, date):
        dates = [date, date]
        values = [0, 0]
        query.prepare('insert into Balance values (null, :value, :date)')
        query.bindValue(':value', values)
        query.bindValue(':date', dates)
        query.execBatch()
        query.clear()

    def create_accounts(self, connect, query):
        if 'Accounts' not in connect.tables():
            query_create_accounts = '''
            create table Accounts (id integer primary key autoincrement,
            value integer, currency text)
            '''
            query.exec(query_create_accounts)
            query.clear()

    def create_category(self, connect, query, name):
        if name not in connect.tables():
            query_create_category = '''
            create table %s (id integer primary key autoincrement, category_en text, category_ru text)
            ''' % name
            query.exec(query_create_category)
            query.clear()
            self.fill_category(query, flag=name)

    def get_category_names(self, flag):
        from menu_languages.menulanguages import MenuLanguages
        en_dict = MenuLanguages.en
        ru_dict = MenuLanguages.ru
        if flag == 'Category_Credit':
            self.en_names = [en_dict[name] for name in MenuLanguages.cat_keys_credit]
            self.ru_names = [ru_dict[name] for name in MenuLanguages.cat_keys_credit]
        else:
            self.en_names = [en_dict[name] for name in MenuLanguages.cat_keys_debit]
            self.ru_names = [ru_dict[name] for name in MenuLanguages.cat_keys_debit]

    def fill_category(self, query, flag):
        self.get_category_names(flag)
        table_name = 'Category_Credit' if flag == 'Category_Credit' else 'Category_Debit'
        query.prepare("insert into %s values (null, :en_names, :ru_names)" % table_name)
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

    def get_current_value(self, start_date: str, name: str, stop_date: str | None, cat_id: int | None = None) -> int:
        value_sum = 0
        connect, query = self.connect_db()
        query_get_current_value = '''
        select sum(value) as value_sum from %s where date>="%s"
        ''' % (name, start_date)
        if stop_date:
            query_get_current_value += ''' and date<="%s"''' % stop_date
        if cat_id:
            query_get_current_value += ''' and cat_id="%d"''' % cat_id
        query.exec(query_get_current_value)
        if query.isActive():
            query.first()
            while query.isValid():
                value_sum = 0 if query.isNull('value_sum') else query.value('value_sum')
                query.next()
                logger.info('get_current_' + name + ': ' + str(value_sum))
        else:
            logger.error('Problem with query: get_current_' + name)
        connect.close()
        return value_sum

    def get_time_span_values(self, start_date: str, table_names: tuple, stop_date: str | None,
                             category: int | None = None) -> list:
        time_span_values = []
        logger.debug('Timespan: ' + start_date)
        connect, query = self.connect_db()
        query_get_span_values = '''
        select cr.id, cr.date, cr.value, cat.%s, cr.note  
        from %s cr join %s cat 
        on cr.cat_id = cat.id
        ''' % (self.category_language, table_names[0], table_names[1])
        where_values = ' where cr.date>="%s"' % start_date if not stop_date \
            else ' where cr.date>="%s" and cr.date<="%s"' % (start_date, stop_date)
        if category:
            where_values = where_values + ' and cr.cat_id="%d"' % category
        query_get_span_values = query_get_span_values + where_values + ' order by cr.date'
        query.exec(query_get_span_values)
        if query.isActive():
            query.first()
            while query.isValid():
                time_span_values.append((query.value('id'), query.value('date'), query.value('value'),
                                               query.value('%s' % self.category_language), query.value('note')))
                query.next()
        else:
            logger.error('Problem with query: get_last_time_span_credits')
        connect.close()
        return time_span_values

    def add_value(self, date: str, value: int, cat_id: int, note: str, id_: None | int,
                  old_value: int, table_name: str, rest=False):
        connect, query = self.connect_db()
        if not id_:
            query.prepare('insert into %s values (null, :date, :value, :cat_id, :note)' % table_name)
            delta_value = value
        else:
            query.prepare('update %s set date=:date, value=:value, cat_id=:cat_id, note=:note where id=:id' % table_name)
            query.bindValue(':id', id_)
            logger.info('Updated record in Credit')
            delta_value = value - old_value
        query.bindValue(':date', date)
        query.bindValue(':value', value)
        query.bindValue(':cat_id', cat_id)
        query.bindValue(':note', note)
        query.exec_()
        query.clear()
        connect.close()
        if not rest:
            self.update_balance(credit=delta_value) if table_name == 'Credit' else self.update_balance(debit=delta_value)
        logger.info('Add new record to ' + table_name)

    def delete_value(self, id_: int, table_name: str, value: int):
        connect, query = self.connect_db()
        query.prepare('delete from %s where id=:id' % table_name)
        query.bindValue(':id', id_)
        query.exec_()
        connect.close()
        self.update_balance(credit=-value) if table_name == 'Credit' else self.update_balance(debit=-value)

    def update_balance(self, credit: int=0, debit: int=0):
        balance = self.get_balance()
        balance = balance + debit - credit
        self.set_balance(balance)

    def get_balance(self, id_=1) -> int | tuple[int, str]:
        balance, date = 0, '0'
        connect, query = self.connect_db()
        query_get_balance = '''
        select balance, date from Balance where id=%d
        ''' % id_
        query.exec(query_get_balance)
        if query.isActive():
            query.first()
            while query.isValid():
                balance = query.value('balance')
                date = query.value('date')
                query.next()
                logger.info('Got Balance: ' + str(balance))
        else:
            logger.error('Problem with query: get_balance')
        connect.close()
        return balance if id_ == 1 else (balance, date)


    def set_balance(self, balance: int, id_=1, date=None):
        connect, query = self.connect_db()
        if id_ == 1:
            query_set_balance = '''
            update Balance set balance=%d where id=1''' % balance
        else:
            query_set_balance = '''
            update Balance set balance=%d, date='%s' where id=2''' % (balance, date)
        query.exec(query_set_balance)
        logger.info('Set Balance: ' + str(balance))
        connect.close()

    def check_month_rest(self, note: str):
        _, old_date = self.get_balance(2)
        if old_date != self.date:
            rest = self.get_balance()
            self.set_balance(rest, 2, self.date)
            self.add_value(self.date, rest, 1, note, None, 0, 'Debit', True)
            logger.info('Month rest changed')

    def get_rest(self, date: str) -> list[tuple[int, str, int, str]]:
        rest = []
        connect, query = self.connect_db()
        query_get_rest = '''
        select id, date, value, cat_id, note 
        from Debit
        where date='%s' and cat_id=1 and note in ('Rest', 'Остаток')
        ''' % date
        query.exec(query_get_rest)
        if query.isActive():
            query.first()
            while query.isValid():
                rest.append((query.value('id'), query.value('date'), query.value('value'), query.value('note')))
                query.next()
                logger.info('Got rest: ' + str(rest))
        else:
            logger.error('Problem with query: get_rest')
        connect.close()
        return rest








