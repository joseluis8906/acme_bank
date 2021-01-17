#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dto import Transaction
from application import CreateAccount, Workflow, StepActionError
from domain import PinValidationError, AccountWithoutBalanceError
from infra import AccountMongoRepo, DollarFakeFetcher
import json
import os
from flask import Flask, request
http = Flask(__name__)

@http.route('/status')
def state():
    return {'data': 'up and running', 'error': None}

@http.route('/accounts', methods=['PUT'])
def create_account():
    data = request.json
    accountRepo = AccountMongoRepo()
    accountCreator = CreateAccount(accountRepo)
    try:
        accountCreator.run(data)
    except Exception as e:
        return {'data': None, 'error': str(e)}
    return {'data': data, 'error': None}


@http.route('/transaction', methods=['POST'])
def transaction():
    data = json.load(request.files['data'])
    transaction = Transaction.from_dict(data)
    accountRepo = AccountMongoRepo()
    dollarFetcher = DollarFakeFetcher()
    workflow = Workflow(accountRepo, accountRepo, dollarFetcher)
    try:
        workflow.run(transaction)
    except PinValidationError as e:
        return {'data': None, 'error': str(e)}
    except AccountWithoutBalanceError as e:
        return {'data': None, 'error': str(e)}
    except StepActionError as e:
        return {'data': None, 'error': str(e)}
    return {'data': 'job done', 'error': None}
        
if __name__ == '__main__':
    http.run(host=os.getenv('ACME_BANK_HOST'), port=os.getenv('ACME_BANK_PORT'))
