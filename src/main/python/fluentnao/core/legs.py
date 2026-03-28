"""Fluent API for controlling NAO robot leg chains (LLeg, RLeg)."""

class Legs():
    """Controls hip and knee joint movements with optional whole body balance.

    Queues leg joint movements using a fluent chaining API. Many methods
    support optional balance via plane constraints to keep the robot stable.
    Most methods only have left_ and right_ variants (no both-legs version)
    because moving both legs simultaneously would cause the robot to fall.

    Hip methods: left_out/right_out, left_in/right_in,
        left_forward/right_forward, left_back/right_back,
        left_up/right_up, left_down/right_down.
    Knee methods: left_knee_bent/right_knee_bent,
        left_knee_straight/right_knee_straight,
        left_knee_up/right_knee_up.
    Balance methods: balance, left_balance, right_balance.
    Stiffness methods: stiff, relax (with left_/right_ variants).

    Args common to positional methods:
        duration: Movement duration in seconds; 0 uses the nao default.
        offset: Degrees added to the base angle for fine adjustment.
        balance: When True (default), enables whole body balance via
            foot plane constraints.

    Sub-objects for chaining: feet.

    Examples::

        nao.legs.left_out().go()
        nao.legs.right_knee_up().go()
        nao.legs.left_forward(2, 10, balance=False).go()
    """

    # init method
    def __init__(self, nao, feet):

        self.feet = feet

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
        """Set both legs to full stiffness."""
        self.left_stiff()
        self.right_stiff()
        return self;

    def left_stiff(self):
        """Set left leg to full stiffness."""
        pNames = self.joints.Chains.LLeg
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def right_stiff(self):
        """Set right leg to full stiffness."""
        pNames = self.joints.Chains.RLeg
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;


    ###################################
    # Relax
    ###################################
    def relax(self):
        """Release both legs (stiffness 0)."""
        self.left_relax()
        self.right_relax()
        return self;

    def left_relax(self):
        """Release left leg (stiffness 0)."""
        pNames = self.joints.Chains.LLeg
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    def right_relax(self):
        """Release right leg (stiffness 0)."""
        pNames = self.joints.Chains.RLeg
        pStiffnessLists = 0
        pTimeLists = 1.0
        self.nao.env.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        return self;

    ###################################
    # Balance
    ###################################
    def left_balance(self, duration=0):
        """Balance on left leg."""
        self.nao.balance(self.joints.SupportLeg.LLeg, duration)
        return self;

    def right_balance(self, duration=0):
        """Balance on right leg."""
        self.nao.balance(self.joints.SupportLeg.RLeg, duration)
        return self;

    def balance(self, duration=0):
        """Balance on both legs."""
        self.nao.balance(self.joints.SupportLeg.Legs, duration)
        return self;


    ###################################
    # Out
    ###################################
    def left_out(self, duration=0, offset=0, balance=True):
        """Move left leg outward (LHipRoll, 35 deg)."""

        if balance:
            self.nao.feet.left_plane_on()

        # move leg out
        duration = self.nao.determine_duration(duration)
        angle = 35 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipRoll, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    def right_out(self, duration=0, offset=0, balance=True):
        """Move right leg outward (RHipRoll, -35 deg)."""

        if balance:
            self.nao.feet.right_plane_on()

        # move leg out
        duration = self.nao.determine_duration(duration)
        angle = -35 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipRoll, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    ###################################
    # In
    ###################################
    def left_in(self, duration=0, offset=0, offset2=0, balance=True):
        """Move left leg inward (LHipPitch + LHipRoll, 0 deg)."""

        if balance:
            self.nao.feet.left_plane_on()

        # move leg in
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        angle2 = 0 + offset2
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipRoll, angle2, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    def right_in(self, duration=0, offset=0, offset2=0, balance=True):
        """Move right leg inward (RHipPitch + RHipRoll, 0 deg)."""

        if balance:
            self.nao.feet.right_plane_on()

        # move leg out
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipRoll, angle2, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    ###################################
    # Forward
    ###################################
    def left_forward(self, duration=0, offset=0, balance=True):
        """Move left leg forward (LHipPitch, -50 deg)."""

        if balance:
            self.nao.feet.left_plane_on()

        # move leg forward
        duration = self.nao.determine_duration(duration)
        angle = -50 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;


    def right_forward(self, duration=0, offset=0, balance=True):
        """Move right leg forward (RHipPitch, -50 deg)."""

        if balance:
            self.nao.feet.right_plane_on()

        # move leg forward
        duration = self.nao.determine_duration(duration)
        angle = -50 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    ###################################
    # Back
    ###################################
    def left_back(self, duration=0, offset=0, balance=True):
        """Move left leg back (LHipPitch, 50 deg)."""

        if balance:
            self.nao.feet.left_plane_on()

        # move leg forward
        duration = self.nao.determine_duration(duration)
        angle = 50 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;


    def right_back(self, duration=0, offset=0, balance=True):
        """Move right leg back (RHipPitch, 50 deg)."""

        if balance:
            self.nao.feet.right_plane_on()

        # move leg forward
        duration = self.nao.determine_duration(duration)
        angle = 50 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)

        if balance:
            self.nao.feet.plane_off()

        return self;

    ###################################
    # Up
    ###################################
    def left_up(self, duration=0, offset=0):
        """Raise left leg (LHipPitch, -90 deg). Auto-balances on right leg."""
        self.right_balance(duration)
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)
        return self;

    def right_up(self, duration=0, offset=0):
        """Raise right leg (RHipPitch, -90 deg). Auto-balances on left leg."""
        self.left_balance(duration)
        duration = self.nao.determine_duration(duration)
        angle = -90 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)
        return self;


    ###################################
    # KneeUp
    ###################################
    def left_knee_up(self, duration=0, offset=0):
        """Raise left leg with bent knee. Balances on right leg."""
        self.right_balance(duration)
        self.left_up(duration, offset)
        self.left_knee_bent(duration, offset)
        return self;

    def right_knee_up(self, duration=0, offset=0):
        """Raise right leg with bent knee. Balances on left leg."""
        self.left_balance(duration)
        self.right_up(duration, offset)
        self.right_knee_bent(duration, offset)
        return self;

    ###################################
    # Down
    ###################################

    def left_down(self, duration=0, offset=0):
        """Lower left leg (LHipPitch, 0 deg)."""
        self.left_balance(duration)
        duration = self.nao.determine_duration(duration)
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LHipPitch, angle, duration)
        return self;

    def right_down(self, duration=0, offset=0):
        """Lower right leg (RHipPitch, 0 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RHipPitch, angle, duration)
        return self;


    ###################################
    # Knee Bent
    ###################################

    def left_knee_bent(self, duration=0, offset=0):
        """Bend left knee (LKneePitch, 90 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LKneePitch, angle, duration)
        return self;

    def right_knee_bent(self, duration=0, offset=0):
        """Bend right knee (RKneePitch, 90 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 90 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RKneePitch, angle, duration)
        return self;


    ###################################
    # Knee Straight
    ###################################

    def left_knee_straight(self, duration=0, offset=0):
        """Straighten left knee (LKneePitch, 0 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LKneePitch, angle, duration)
        return self;

    def right_knee_straight(self, duration=0, offset=0):
        """Straighten right knee (RKneePitch, 0 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RKneePitch, angle, duration)
        return self;

