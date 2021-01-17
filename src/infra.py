#!/usr/bin/env python
# -*- coding: utf-8 -*-

from domain import Account
from application import AccountGetter, AccountSaver, DollarFetcher
from pymongo import MongoClient
import os


class AccountInMemoryRepo(AccountGetter, AccountSaver):
    def __init__(self):
        self.data = []

    def get_by_id(self, id: str) -> Account:
        return next(filter(lambda elm: elm.id() == id, self.data), None)

    def save(self, account: Account):
        exists = next(filter(lambda elm: elm.id() == account.id(), self.data),
                      None)
        if exists is not None:
            self.data = [
                account if elem.id() == elem.id() else elem
                for elem in self.data
            ]
        else:
            self.data.append(account)


class AccountMongoRepo(AccountGetter, AccountSaver):
    def __init__(self):
        self._client = MongoClient('mongodb://{}:{}@{}:{}/'.format(
            os.getenv('MONGO_INITDB_ROOT_USERNAME'),
            os.getenv('MONGO_INITDB_ROOT_PASSWORD'), os.getenv('MONGO_HOST'),
            os.getenv('MONGO_PORT')))
        self._db = self._client[os.getenv('MONGO_DB')]
        self._accounts = self._db['accounts']
        self._accounts.create_index('user_id', unique=True)

    def get_by_id(self, id: str) -> Account:
        return Account.from_dict(self._accounts.find_one({'user_id': id}))

    def save(self, account: Account):
        self._accounts.update({'user_id': account.id()},
                              account.to_dict(),
                              upsert=True)


class DollarFakeFetcher(DollarFetcher):
    def fetch(self) -> float:
        return 3459
