#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PinValidationError(Exception):
    pass

class PinChangingError(Exception):
    pass

class AccountWithoutBalanceError(Exception):
    pass

class Account:
    def __init__(self, id: str, pin: str, balance: float):
        self._id = id
        self._pin = pin
        self._balance = balance

    def id(self) -> str:
        return self._id

    def verify_pin(self, pin) -> bool:
        if not isinstance(pin, str):
            pin = str(pin)
        if self._pin != pin:
            raise PinValidationError('invalid pin')
        return True

    def update_pin(self, pin: str) -> None:
        if self._pin == pin:
            raise PinChangingError('old and new pin are the same')
        self._pin = pin

    def balance(self) -> float:
        return self._balance

    def add_balance(self, amount: float) -> None:
        self._balance += amount

    def sub_balance(self, amount: float) -> None:
        if self._balance < amount:
            raise AccountWithoutBalanceError('insufficient balance')
        self._balance -= amount

    def to_dict(self):
        return dict(user_id=self._id, pin=self._pin, balance=self._balance)

    @classmethod
    def from_dict(cls, raw: dict):
        return cls(raw['user_id'], raw['pin'], int(raw['balance']))

