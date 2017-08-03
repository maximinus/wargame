#!/usr/bin/env python3

from enum import Enum


class Align(Enum):
    """
    Where to align GUI nodes
    """
    TOP_LEFT = 0
    TOP_CENTRE = 1
    TOP_RIGHT = 2
    CENTRE_LEFT = 3
    CENTRE = 4
    CENTRE_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_CENTRE = 7
    BOTTOM_RIGHT = 8
    NONE = 9
