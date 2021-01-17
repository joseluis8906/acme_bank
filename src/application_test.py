#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from dto import Transaction, Step, Trigger
from infra import AccountInMemoryRepo, DollarFakeFetcher
from domain import Account
from application import Workflow, StepActionError

class TestWorkflow(unittest.TestCase):
    def test_exec_without_errors(self):
        trigger = Trigger({'user_id': '10', 'pin': '1234'}, None, None)
        steps = [
            Step(None, None, 'validate_account', None),
            Step(None, None, 'get_account_balance', None),
            Step(None, {'money': {'value': 10000}}, 'withdraw_in_pesos', None),
            Step(None, {'money': {'value': 3}}, 'withdraw_in_dollars', None),
        ]
        transaction = Transaction(steps, trigger)
        accountRepo = AccountInMemoryRepo()
        accountRepo.save(Account('10', '1234', 50000))
        dollarFetcher = DollarFakeFetcher()
        workflow = Workflow(accountRepo, accountRepo, dollarFetcher)
        workflow.run(transaction)
        account = accountRepo.get_by_id('10')
        self.assertEqual(account.balance(), 29623)

    def test_exec_return_error(self):
        with self.assertRaises(StepActionError):
            trigger = Trigger({'user_id': '11', 'pin': '4321'}, None, None)
            steps = [
                Step(None, None, 'validate_account', None),
                Step(None, None, 'get_account_balance', None),
                Step(None, {'money': {'value': 10000}}, 'withdraw_in_pesos', None),
                Step(None, {'money': {'value': 3}}, 'withdraw_in_euros', None),
            ]
            transaction = Transaction(steps, trigger)
            accountRepo = AccountInMemoryRepo()
            accountRepo.save(Account('11', '4321', 50000))
            dollarFetcher = DollarFakeFetcher()
            workflow = Workflow(accountRepo, accountRepo, dollarFetcher)
            workflow.run(transaction)
            account = accountRepo.get_by_id('10')
            self.assertEqual(account.balance(), 29623)
        
