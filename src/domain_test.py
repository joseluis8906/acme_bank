#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from domain import Account, AccountWithoutBalanceError, PinValidationError, PinChangingError

class TestAccount(unittest.TestCase):
    def test_modify_balance(self):
        account = Account('1', '1234', 100)
        account.add_balance(20)
        account.sub_balance(80)
        self.assertEqual(account.balance(), 40)

    def test_modify_balance_return_error(self):
        with self.assertRaises(AccountWithoutBalanceError):
            account = Account('1', '1234', 100)
            self.assertEqual(account.sub_balance(120))

    def test_validate_pin_without_errors(self):
        account = Account('1', '1234', 100)
        self.assertTrue(account.verify_pin('1234'))
    
    def test_validate_pin_return_error(self):
        with self.assertRaises(PinValidationError):
            account = Account('1', '1234', 100)
            self.assertTrue(account.verify_pin('4321'))
    
    def test_modify_pin_without_errors(self):
        account = Account('1', '1234', 100)
        self.assertIsNone(account.update_pin('4321'))

    def test_modify_pin_return_error(self):
        with self.assertRaises(PinChangingError):
            account = Account('1', '1234', 100)
            account.update_pin('4321')
            self.assertIsNone(account.update_pin('4321'))
        

