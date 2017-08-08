#!/usr/bin/env python3

import pygame

# for us to be able to tween something, it must be some displayable
# image. That means, it needs an image and a rect
# tweens are NOT updated every X seconds or so
# they are merely sent the value of the time NOW
# So you record the time you get on the FIRST update,
# and use that to figure out what to update


class TweenObject:
    def __init__(self, start=None):
        self.start = start
        self.time_passed = 0

    def update(self):
        # nothing to update
        return TweenResult()


class TweenResult:
    def __init__(self, new=None, old=None, time_left=0):
        # new - draw me as well
        # old - do not draw me
        self.new = new
        self.old = old
        self.time_left = time_left

    @property
    def finished(self):
        # if we didn't use up all our time
        return self.time_left != 0

    def __repr__(self):
        return '<{0}->{1}>:{2}'.format(self.old, self.new, self.time_left)


class FlashTween(TweenObject):
    """
    A flash tween will turn the visibility off/on
    """
    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.display = True

    def update(self, node, time_delta):
        # the delay is the length of time we wait
        self.time_passed += time_delta
        if self.time_passed < self.delay:
            # no need to update, unless we have changed from last time
            if self.display:
                self.display = False
                return TweenResult(new=node.rect)
            return TweenResult()
        # sort out the time delay
        self.time_passed = self.time_passed % self.delay
        node.visible = not node.visible
        self.display = True
        return TweenResult(new=node.rect)


class MoveTween(TweenObject):
    def __init__(self, time, start_pos, vector):
        super().__init__()
        self.time = time
        self.start = start_pos.copy()
        self.vector = vector

    def update(self, node, time_delta):
        # move from a to b
        # what position should we be at at this time?
        current_pos = node.rect.copy()
        self.time_passed += time_delta
        # have we ended?
        if self.time_passed >= self.time:
            return self.end_tween(current_pos, node)
        x_delta = int(self.vector.x * (self.time_passed / self.time))
        y_delta = int(self.vector.y * (self.time_passed / self.time))
        xpos = x_delta + self.start.x
        ypos = y_delta + self.start.y
        if xpos != current_pos.x or ypos != current_pos.y:
            # we've moved
            new_pos = pygame.Rect(xpos, ypos, current_pos.width, current_pos.height)
            node.rect = new_pos
            return TweenResult(new=new_pos, old=current_pos)
        # nothing
        return TweenResult()

    def end_tween(self, current_pos, node):
        time_left = self.time_passed - self.time
        # drawn up to the end?
        endx = self.start.x + self.vector.x
        endy = self.start.y + self.vector.y
        if endx != current_pos.x or endy != current_pos.y:
            # we need to update
            node.rect = pygame.Rect(endx, endy, current_pos.width, current_pos.height)
            return TweenResult(new=node.rect, old=current_pos, time_left=time_left)
        # no need to update anything
        return TweenResult(time_left=time_left)


class PauseTween(TweenObject):
    def __init__(self, delay):
        self.delay = delay
        super().__init__()

    def update(self, time_delta):
        self.time_passed += time_delta
        if self.time_passed >= self.delay:
            # finished
            return TweenResult(time_left=self.time_passed - self.delay)
        return(TweenResult())


class ChainedTween(TweenObject):
    """
    This tween allows you to chain several tweens together
    """
    def __init__(self, tweens, loop=False):
        self.tweens = tweens
        self.index = 0
        self.loop = loop

    def update(self, node, time_delta):
        result = self.tweens[self.index].update(node, time_delta)
        # are we finished?
        if not result.finished:
            # no, just return the result
            return(result)
        # yes, we need move to the next tween
        return self.move_to_next_tween(node, result)

    def move_to_next_tween(self, node, result):
        while(result.time_left > 0):
            # move to next tween
            self.index += 1
            if self.index >= len(self.tweens):
                # at the end. Do we loop?
                if not self.loop:
                    # we really are done
                    return result
                # loop to start
                self.index = 0
            # we've moved to the next tween
            # we need to tell the next tween where and where it starts
            self.tweens[self.index].time_passed = 0
            self.tweens[self.index].start = node.rect.copy()
            result2 = self.tweens[self.index].update(node, result.time_left)
            # only update the new position
            result.new = result2.new
            result.time_left = result2.time_left
        # if we drop here, we have finished all tween results
        return result
