#!/usr/bin/env python3

from enum import Enum


class Layout(Enum):
    LEFT = 0
    CENTRE = 1
    RIGHT = 2
    BETWEEN = 3
    AROUND = 4


class Align(Enum):
    LEFT = 0
    CENTRE = 1
    RIGHT = 2
