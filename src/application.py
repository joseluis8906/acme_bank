#!/usr/bin/env python
# -*- coding: utf-8 -*-

from domain import Account, PinValidationError, AccountWithoutBalanceError
from dto import Transaction


class StepActionError(Exception):
    pass


class AccountSaver:
    def save(self, account: Account):
        raise Exception('method not implemented')


class AccountGetter:
    def get_by_id(self, id: str) -> Account:
        raise Exception('method not implemented')


class DollarFetcher:
    def fetch(self) -> float:
        raise Exception('method not implemented')


class Workflow:
    def __init__(self, account_getter: AccountGetter,
                 account_saver: AccountSaver, dollar_fetcher: DollarFetcher):
        self.account = None
        self.transaction = None
        self.account_getter = account_getter
        self.account_saver = account_saver
        self.dollar_fetcher = dollar_fetcher

    def _get_account(self):
        self.account = self.account_getter.get_by_id(
            self.transaction.trigger.params['user_id'])

    def _validate_account(self):
        self.account.verify_pin(self.transaction.trigger.params['pin'])

    def _get_account_balance(self):
        print('balance: ', self.account.balance())

    def _deposit_money(self, cop_amount: float):
        self.account.add_balance(cop_amount)

    def _withdraw_in_pesos(self, cop_amount: float):
        self.account.sub_balance(cop_amount)

    def _withdraw_in_dollars(self, usd_amount: float):
        amount_in_pesos = usd_amount * self.dollar_fetcher.fetch()
        self.account.sub_balance(amount_in_pesos)

    def run(self, transaction: Transaction):
        self.transaction = transaction
        self._get_account()
        for step in self.transaction.steps:
            if step.action == 'validate_account':
                self._validate_account()
            elif step.action == 'get_account_balance':
                self._get_account_balance()
            elif step.action == 'deposit_money':
                self._deposit_money(step.params['money']['value'])
            elif step.action == 'withdraw_in_pesos':
                self._withdraw_in_pesos(step.params['money']['value'])
            elif step.action == 'withdraw_in_dollars':
                self._withdraw_in_dollars(step.params['money']['value'])
            else:
                raise StepActionError('invalid action {}'.format(step.action))

        self.account_saver.save(self.account)


class CreateAccount:
    def __init__(self, account_saver: AccountSaver):
        self.account_saver = account_saver

    def run(self, data: dict):
        self.account_saver.save(Account.from_dict(data))
