"""Fluent API for controlling NAO robot shoulder joints (LArm, RArm)."""

class Arms():
    """Controls both arm chains via ShoulderPitch and ShoulderRoll joints.

    Queues shoulder joint movements using a fluent chaining API. Moves are
    queued until go() is called, which executes them and returns the
    top-level nao object so you can continue chaining other body parts.

    Positional methods (both arms):
        up, down, forward, out, back -- each with left_ and right_ variants.

    Args common to positional methods:
        duration: Movement duration in seconds; 0 uses the nao default.
        offset: Degrees added to the primary angle (ShoulderPitch).
        offset2: Degrees added to the secondary angle (ShoulderRoll).

    Left and right offsets are mirrored automatically so the same offset
    value produces symmetric movement.

    Sub-objects for chaining: elbows, wrists, hands.

    Examples::

        nao.arms.up().go()
        nao.arms.left_forward(2, 15).right_out().go()
        nao.arms.up().elbows.bent().go()
        nao.arms.relax()
    """

    # init method
    def __init__(self, nao, elbows, wrists, hands):

        self.elbows = elbows
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
    # Stiff
    ###################################
    def stiff(self):
        """Set both arms to full stiffness."""
        self.left_stiff()
        self.right_stiff()
        return self;

    def left_stiff(self):
        """Set left arm to full stiffness."""
        pNames = self.joints.Chains.LArm
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def right_stiff(self):
        """Set right arm to full stiffness."""
        pNames = self.joints.Chains.RArm
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;


    ###################################
    # Relax
    ###################################
    def relax(self):
        """Release both arms (stiffness 0)."""
        self.left_relax()
        self.right_relax()
        return self;

    def left_relax(self):
        """Release left arm (stiffness 0)."""
        pNames = self.joints.Chains.LArm
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def right_relax(self):
        """Release right arm (stiffness 0)."""
        pNames = self.joints.Chains.RArm
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    ###################################
    # Forward
    ###################################
    def forward(self, duration=0, offset=0, offset2=0):
        """Move both arms forward (0 deg pitch)."""
        self.right_forward(duration, offset, offset2)
        self.left_forward(duration, offset, offset2)
        return self;

    def left_forward(self, duration=0, offset=0, offset2=0):
        """Move left arm forward (0 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)

        return self;

    def right_forward(self, duration=0, offset=0, offset2=0):
        """Move right arm forward (0 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;

    ###################################
    # Out
    ###################################
    def out(self, duration=0, offset=0, offset2=0):
        """Move both arms out to sides (90 deg roll)."""
        self.right_out(duration, offset, offset2)
        self.left_out(duration, offset, offset2)
        return self;

    def left_out(self, duration=0, offset=0, offset2=0):
        """Move left arm out to side (90 deg roll)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        angle2 = 90 + offset2

        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)
        return self;

    def right_out(self, duration=0, offset=0, offset2=0):
        """Move right arm out to side (-90 deg roll)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        angle2 = -90 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;

    ###################################
    # Up
    ###################################
    def up(self, duration=0, offset=0, offset2=0):
        """Move both arms straight up (-90 deg pitch)."""
        self.right_up(duration, offset, offset2)
        self.left_up(duration, offset, offset2)
        return self;

    def left_up(self, duration=0, offset=0, offset2=0):
        """Move left arm straight up (-90 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)
        return self;

    def right_up(self, duration=0, offset=0, offset2=0):
        """Move right arm straight up (-90 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;

    ###################################
    # Down
    ###################################
    def down(self, duration=0, offset=0, offset2=0):
        """Move both arms straight down (90 deg pitch)."""
        self.right_down(duration, offset, offset2)
        self.left_down(duration, offset, offset2)
        return self;

    def left_down(self, duration=0, offset=0, offset2=0):
        """Move left arm straight down (90 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)
        return self;

    def right_down(self, duration=0, offset=0, offset2=0):
        """Move right arm straight down (90 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;


    ###################################
    # Back
    ###################################
    def back(self, duration=0, offset=0, offset2=0):
        """Move both arms behind (119.5 deg pitch)."""
        self.right_back(duration, offset, offset2)
        self.left_back(duration, offset, offset2)
        return self;

    def left_back(self, duration=0, offset=0, offset2=0):
        """Move left arm behind (119.5 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = 119.5 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LArm.LShoulderRoll, angle2, duration)
        return self;

    def right_back(self, duration=0, offset=0, offset2=0):
        """Move right arm behind (119.5 deg pitch)."""
        duration = self.nao.determine_duration(duration)
        angle = 119.5 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RArm.RShoulderRoll, angle2, duration)
        return self;