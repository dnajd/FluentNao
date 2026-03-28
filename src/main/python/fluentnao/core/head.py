"""Fluent API for controlling NAO robot head yaw and pitch joints."""

class Head():
    """Controls head yaw (horizontal) and pitch (vertical) movements.

    Queues head joint movements using a fluent chaining API. Moves are
    queued until go() is called.

    Yaw methods: left, right, forward.
    Pitch methods: up, down, center.
    Stiffness methods: stiff, relax.

    Args common to positional methods:
        duration: Movement duration in seconds; 0 uses the nao default.
        offset: Degrees added to the base angle for fine adjustment.

    The head has no left_/right_ sub-variants since there is only one head.

    Examples::

        nao.head.left().go()
        nao.head.up(0, -15).go()
        nao.head.forward().down(0, 5).go()
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
    # Stiff
    ###################################
    def stiff(self):
        """Set head to full stiffness."""
        pNames = self.joints.Chains.Head
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    ###################################
    # Relax
    ###################################
    def relax(self):
        """Release head (stiffness 0)."""
        pNames = self.joints.Chains.Head
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    ###################################
    # turn
    ###################################
    def left(self, duration=0, offset=0):
        """Turn head left (90 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)
        return self;

    def right(self, duration=0, offset=0):
        """Turn head right (-90 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)
        return self;

    def forward(self, duration=0, offset=0):
        """Face head forward (0 deg yaw)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadYaw, angle, duration)
        return self;


    ###################################
    # up / down
    ###################################

    def up(self, duration=0, offset=0):
        """Tilt head up (-38 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = -38 - offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)
        return self;

    def down(self, duration=0, offset=0):
        """Tilt head down (29 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = 29 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)
        return self;

    def center(self, duration=0, offset=0):
        """Center head pitch (0 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.Head.HeadPitch, angle, duration)
        return self;