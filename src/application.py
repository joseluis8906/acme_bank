#!/usr/bin/env python
# -*- coding: utf-8 -*-

from domain import Account, PinValidationError, AccountWithoutBalanceError
from dto import Transaction

class StepActionError(Exception):
    pass

class AccountSaver:
    def save(account: Account):
        raise Exception('method not implemented')

class AccountGetter:
    def get_by_id(id: str) -> Account:
        raise Exception('method not implemented')

class DollarFetcher:
    def fetch() -> float:
        raise Exception('method not implemented')

class Workflow:
    def __init__(self, accountGetter: AccountGetter, accountSaver: AccountSaver, dollarFetcher: DollarFetcher):
        self.account = None
        self.transaction = None
        self.accountGetter = accountGetter
        self.accountSaver = accountSaver
        self.dollarFetcher = dollarFetcher

    def _get_account(self):
        self.account = self.accountGetter.get_by_id(self.transaction.trigger.params['user_id'])

    def _validate_account(self):
        self.account.verify_pin(self.transaction.trigger.params['pin'])

    def _get_account_balance(self):
        print('balance: ', self.account.balance())

    def _deposit_money(self, cop_amount: float):
        self.account.add_balance(cop_amount)

    def _withdraw_in_pesos(self, cop_amount: float):
        self.account.sub_balance(cop_amount)

    def _withdraw_in_dollars(self, usd_amount: float):
        amount_in_pesos = usd_amount * self.dollarFetcher.fetch()
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

        self.accountSaver.save(self.account)

class CreateAccount:
    def __init__(self, accountSaver: AccountSaver):
        self.accountSaver = accountSaver

    def run(self, data: dict):
        self.accountSaver.save(Account.from_dict(data))

