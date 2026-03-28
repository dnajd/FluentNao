"""Fluent API for controlling NAO robot wrist rotation (WristYaw)."""

class Wrists():
    """Controls wrist yaw movements for both arms.

    Queues wrist yaw movements using a fluent chaining API. Moves are
    queued until go() is called.

    Methods: center, turn_out, turn_in -- each with left_ and right_ variants.

    Args common to all positional methods:
        duration: Movement duration in seconds; 0 uses the nao default.
        offset: Degrees added to the base angle for fine adjustment.

    Left and right angles are mirrored automatically so the same offset
    produces symmetric movement.

    Sub-objects for chaining: hands.

    Examples::

        nao.wrists.turn_out().go()
        nao.wrists.left_center().go()
        nao.arms.forward().wrists.turn_in().go()
    """

    # init method
    def __init__(self, nao, hands):

        self.hands = hands

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
    # Center
    ###################################
    def center(self, duration=0, offset=0):
        """Center both wrists (0 deg yaw)."""
        self.left_center(duration, offset)
        self.right_center(duration, offset)
        return self;

    def left_center(self, duration=0, offset=0):
        """Center left wrist (0 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = 0.0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;

    def right_center(self, duration=0, offset=0):
        """Center right wrist (0 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = 0.0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;

    ###################################
    # Out
    ###################################
    def turn_out(self, duration=0, offset=0):
        """Rotate both wrists outward (90 deg)."""
        self.left_turn_out(duration, offset)
        self.right_turn_out(duration, offset)
        return self;

    def left_turn_out(self, duration=0, offset=0):
        """Rotate left wrist outward (90 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;

    def right_turn_out(self, duration=0, offset=0):
        """Rotate right wrist outward (-90 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;

    ###################################
    # In
    ###################################
    def turn_in(self, duration=0, offset=0):
        """Rotate both wrists inward (-90 deg)."""
        self.left_turn_in(duration, offset)
        self.right_turn_in(duration, offset)
        return self;

    def left_turn_in(self, duration=0, offset=0):
        """Rotate left wrist inward (-90 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LWristYaw, angle, duration)
        return self;

    def right_turn_in(self, duration=0, offset=0):
        """Rotate right wrist inward (90 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RWristYaw, angle, duration)
        return self;