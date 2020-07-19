#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import Union, Callable, Optional

from nonebot.event import Event


class Rule:

    def __init__(self, checker: Optional[Callable[[Event], bool]] = None):
        self.checker = checker or (lambda event: True)

    def __call__(self, event: Event) -> bool:
        return self.checker(event)

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(lambda event: self.checker(event) and other.checker(event))

    def __or__(self, other: "Rule") -> "Rule":
        return Rule(lambda event: self.checker(event) or other.checker(event))

    def __neg__(self) -> "Rule":
        return Rule(lambda event: not self.checker(event))


def user(*qq: int) -> Rule:
    return Rule(lambda event: event.user_id in qq)


def private() -> Rule:
    return Rule(lambda event: event.detail_type == "private")


def group(*group: int) -> Rule:
    return Rule(
        lambda event: event.detail_type == "group" and event.group_id in group)


def discuss(*discuss: int) -> Rule:
    return Rule(lambda event: event.detail_type == "discuss" and event.
                discuss_id in discuss)


def startswith(msg, start: int = None, end: int = None) -> Rule:
    return Rule(lambda event: event.message.startswith(msg, start, end))


def endswith(msg, start: int = None, end: int = None) -> Rule:
    return Rule(lambda event: event.message.endswith(msg, start=None, end=None))


def has(msg: str) -> Rule:
    return Rule(lambda event: msg in event.message)


def regex(regex, flags: Union[int, re.RegexFlag] = 0) -> Rule:
    pattern = re.compile(regex, flags)
    return Rule(lambda event: bool(pattern.search(event.message)))