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
    account_repo = AccountMongoRepo()
    account_creator = CreateAccount(account_repo)
    try:
        account_creator.run(data)
    except Exception as err:
        return {'data': None, 'error': str(err)}
    return {'data': data, 'error': None}


@http.route('/transactions', methods=['POST'])
def transactions():
    data = json.load(request.files['data'])
    transaction = Transaction.from_dict(data)
    account_repo = AccountMongoRepo()
    dollar_fetcher = DollarFakeFetcher()
    workflow = Workflow(account_repo, account_repo, dollar_fetcher)
    try:
        workflow.run(transaction)
    except PinValidationError as err:
        return {'data': None, 'error': str(err)}
    except AccountWithoutBalanceError as err:
        return {'data': None, 'error': str(err)}
    except StepActionError as err:
        return {'data': None, 'error': str(err)}
    return {'data': 'job done', 'error': None}


if __name__ == '__main__':
    http.run(host=os.getenv('ACME_BANK_HOST'),
             port=os.getenv('ACME_BANK_PORT'))
