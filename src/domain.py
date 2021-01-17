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
        self.__id = id
        self.__pin = pin
        self.__balance = balance

    def id(self) -> str:
        return self.__id

    def verify_pin(self, pin) -> bool:
        if not isinstance(pin, str):
            pin = str(pin)
        if self.__pin != pin:
            raise PinValidationError('invalid pin')
        return True

    def update_pin(self, pin: str) -> None:
        if self.__pin == pin:
            raise PinChangingError('old and new pin are the same')
        self.__pin = pin

    def balance(self) -> float:
        return self.__balance

    def add_balance(self, amount: float) -> None:
        self.__balance += amount

    def sub_balance(self, amount: float) -> None:
        if self.__balance < amount:
            raise AccountWithoutBalanceError('insufficient balance')
        self.__balance -= amount

    def to_dict(self):
        return dict(user_id=self.__id, pin=self.__pin, balance=self.__balance)

    @classmethod
    def from_dict(cls, raw: dict):
        return cls(raw['user_id'], raw['pin'], int(raw['balance']))
