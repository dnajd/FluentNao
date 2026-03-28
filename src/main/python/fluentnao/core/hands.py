"""Fluent API for controlling NAO robot hand open/close."""

import math

class Hands():
    """Controls hand open and close movements for both hands.

    Queues hand movements using a fluent chaining API. Moves are queued
    until go() is called.

    Methods: open, close -- each with left_ and right_ variants.

    Args common to all methods:
        duration: Movement duration in seconds; 0 uses the nao default.

    Hand values are passed through math.degrees() -- 1.0 for open, 0.0
    for close.

    Examples::

        nao.hands.open().go()
        nao.hands.right_close().go()
        nao.arms.out().hands.open().go()
    """

    # init method
    def __init__(self, nao):

        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

    def go(self):
        """Execute all queued moves and return the nao object."""
        self.nao.go()
        return self.nao

    ###################################
    # Hands Open
    ###################################
    def open(self, duration=0):
        """Open both hands fully."""
        self.right_open(duration)
        self.left_open(duration)
        return self;

    def left_open(self, duration=0):
        """Open left hand fully."""
        duration = self.nao.determine_duration(duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LHand, math.degrees(1.0), duration)
        return self;

    def right_open(self, duration=0):
        """Open right hand fully."""
        duration = self.nao.determine_duration(duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RHand, math.degrees(1.0), duration)
        return self;

    ###################################
    # Hands Close
    ###################################
    def close(self, duration=0):
        """Close both hands fully."""
        self.right_close(duration)
        self.left_close(duration)
        return self;

    def left_close(self, duration=0):
        """Close left hand fully."""
        duration = self.nao.determine_duration(duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LHand, math.degrees(0.0), duration)
        return self;

    def right_close(self, duration=0):
        """Close right hand fully."""
        duration = self.nao.determine_duration(duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RHand, math.degrees(0.0), duration)
        return self;