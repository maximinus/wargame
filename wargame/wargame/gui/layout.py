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
    LEFT = 10
    RIGHT = 11
    TOP = 12
    BOTTOM = 13
    AROUND = 14
    BETWEEN = 15

    @staticmethod
    def horizontal(align):
        if align in [Align.TOP_LEFT, Align.CENTRE_LEFT, Align.BOTTOM_LEFT]:
            return Align.LEFT
        if align in [Align.TOP_RIGHT, Align.CENTRE_RIGHT, Align.BOTTOM_CENTRE]:
            return Align.RIGHT
        # default is centre
        return Align.CENTRE

    @staticmethod
    def vertical(align):
        if align in [Align.TOP_LEFT, Align.TOP_CENTRE, Align.TOP_RIGHT, Align.TOP]:
            return Align.TOP
        if align in [Align.BOTTOM_LEFT, Align.BOTTOM_CENTRE, Align.BOTTOM_RIGHT, Align.BOTTOM]:
            return Align.BOTTOM
        # default is centre
        return Align.CENTRE
