#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Param:
    def __init__(self, from_id: str, param_id: str):
        self.from_id = from_id
        self.param_id = param_id

    @classmethod
    def from_dict(cls, raw: dict):
        return cls(raw['from_id'], raw['param_id'])

    def to_dict(self):
        return dict(from_id=self.from_id, param_id=self.param_id)

class Condition:
    def __init__(self, from_id: str, field_id: str, operator: str, value: any):
        self.from_id = from_id
        self.field_id = field_id
        self.operator = operator
        self.value = value

    @classmethod
    def from_dict(cls, raw: dict):
        return cls(raw['from_id'], raw['field_id'], raw['operator'], raw['value'])

    def to_dict(self):
        return dict(from_id=self.from_id, field_id=self.field_id, operator=self.operator, value=self.value)

class Transition:
    def __init__(self, conditions: [Condition], target: str):
        self.conditions = conditions
        self.target = target

    @classmethod
    def from_dict(cls, raw: dict):
        conditions = []
        for c in raw['condition']:
            conditions.append(Condition.from_dict(c))
        return cls(conditions, raw['target'])

    def to_dict(self):
        return dict(condition=self.conditions, target=self.target)

class Step:
    def __init__(self, id: str, params: dict, action: str, transitions: [Transition]):
        self.id = id
        self.params = params
        self.action = action
        self.transitions = transitions

    @classmethod
    def from_dict(cls, raw: dict):
        transitions = []
        for t in raw['transitions']:
            transitions.append(Transition.from_dict(t))
        return cls(raw['id'], raw['params'], raw['action'], transitions)


    def to_dict(self):
        return dict(id=self.id, params=self.params, action=self.action, transitions=self.transitions)

class Trigger:
    def __init__(self, params: dict, transitions: [Transition], id_: str):
        self.params = params
        self.transitions = transitions
        self.id = id_

    @classmethod
    def from_dict(cls, raw: dict):
        transitions = []
        for t in raw['transitions']:
            transitions.append(Transition.from_dict(t))
        return cls(raw['params'], transitions, raw['id'])

    def to_dict(self):
        return dict(params=self.params, transitions=self.transitions, id=self.id)

class Transaction:
    def __init__(self, steps: [Step], trigger: Trigger):
        self.steps = steps
        self.trigger = trigger
    
    @classmethod
    def from_dict(cls, raw: dict):
        steps = []
        for s in raw['steps']:
            steps.append(Step.from_dict(s))
        trigger = Trigger.from_dict(raw['trigger'])
        return cls(steps, trigger)

    def to_dict(self):
        return dict(steps=self.steps, trigger=self.trigger)

