"""Fluent API for controlling NAO robot elbow joints (ElbowRoll, ElbowYaw)."""

class Elbows():
    """Controls elbow flex (roll) and rotation (yaw) movements.

    Queues elbow joint movements using a fluent chaining API. Moves are
    queued until go() is called.

    Flex methods (ElbowRoll): bent, straight.
    Rotation methods (ElbowYaw): turn_up, turn_down, turn_in.
    Each has left_ and right_ variants.

    Args common to all positional methods:
        duration: Movement duration in seconds; 0 uses the nao default.
        offset: Degrees added to the base angle for fine adjustment.

    Left and right angles are automatically mirrored so the same offset
    produces symmetric movement.

    Sub-objects for chaining: wrists, hands.

    Examples::

        nao.elbows.bent().go()
        nao.arms.up().elbows.bent().go()
        nao.elbows.right_bent(0, 10).go()
    """

    # init method
    def __init__(self, nao, wrists, hands):

        self.wrists = wrists
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
    # Bent
    ###################################
    def bent(self, duration=0, offset=0):
        """Bend both elbows to 89 degrees."""
        self.right_bent(duration, offset)
        self.left_bent(duration, offset)
        return self;

    def right_bent(self, duration=0, offset=0):
        """Bend right elbow to 89 degrees."""
        duration = self.nao.determine_duration(duration)
        angle = 89 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowRoll, angle, duration)
        return self;


    def left_bent(self, duration=0, offset=0):
        """Bend left elbow to -89 degrees."""
        duration = self.nao.determine_duration(duration)
        angle = -89 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowRoll, angle, duration)
        return self;

    ###################################
    # Straight
    ###################################
    def straight(self, duration=0, offset=0):
        """Straighten both elbows to ~0.5 degrees."""
        self.right_straight(duration, offset)
        self.left_straight(duration, offset)
        return self;

    def right_straight(self, duration=0, offset=0):
        """Straighten right elbow to ~0.5 degrees."""
        duration = self.nao.determine_duration(duration)
        angle = 0.5 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowRoll, angle, duration)
        return self;


    def left_straight(self, duration=0, offset=0):
        """Straighten left elbow to ~0.5 degrees."""
        duration = self.nao.determine_duration(duration)
        angle = 0.5 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowRoll, angle, duration)
        return self;


    ###################################
    # Up
    ###################################
    def turn_up(self, duration=0, offset=0):
        """Rotate both elbows up (90 deg yaw)."""
        self.right_turn_up(duration, offset)
        self.left_turn_up(duration, offset)
        return self;

    def right_turn_up(self, duration=0, offset=0):
        """Rotate right elbow up (90 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;


    def left_turn_up(self, duration=0, offset=0):
        """Rotate left elbow up (-90 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;

    ###################################
    # Turn Down
    ###################################
    def turn_down(self, duration=0, offset=0):
        """Rotate both elbows down (-90 deg yaw)."""
        self.right_turn_down(duration, offset)
        self.left_turn_down(duration, offset)
        return self;

    def right_turn_down(self, duration=0, offset=0):
        """Rotate right elbow down (-90 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;

    def left_turn_down(self, duration=0, offset=0):
        """Rotate left elbow down (90 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;


    ###################################
    # In
    ###################################
    def turn_in(self, duration=0, offset=0):
        """Rotate both elbows inward (0 deg yaw)."""
        self.right_turn_in(duration, offset)
        self.left_turn_in(duration, offset)
        return self;

    def right_turn_in(self, duration=0, offset=0):
        """Rotate right elbow inward (0 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RElbowYaw, angle, duration)
        return self;

    def left_turn_in(self, duration=0, offset=0):
        """Rotate left elbow inward (0 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LElbowYaw, angle, duration)
        return self;