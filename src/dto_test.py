#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from dto import Transaction
from utils import ComplexEncoder
import json

class TestTransaction(unittest.TestCase):
    def test_parse_from_and_to_json(self):
        with  open('../assets/obj.json') as json_file:
            data = json.load(json_file)
            transaction = Transaction.from_dict(data)
            json_transaction = json.loads(json.dumps(transaction.to_dict(), cls=ComplexEncoder))
            self.assertEqual(data, json_transaction)
