"""Fluent API for controlling NAO robot ankle joints and balance plane constraints."""

class Feet():
    """Controls ankle pitch/roll movements and whole body balance constraints.

    Queues ankle pitch and roll movements using a fluent chaining API.
    Also manages whole body balance plane constraints used by the Legs class.

    Ankle pitch methods: point_toes, raise_toes.
    Ankle roll methods: turn_out, turn_in.
    Center method: center (sets both roll and pitch to 0).
    Each has left_ and right_ variants.

    Plane constraint methods (used internally by Legs):
        left_plane_on, right_plane_on, plane_off.
        These do NOT return self and are not meant for fluent chaining.
        plane_off() calls go() internally before releasing constraints.

    Args common to ankle methods:
        duration: Movement duration in seconds; 0 uses the nao default.
        offset: Degrees added to the primary angle.
        offset2: Degrees added to the secondary angle (center() only).

    Examples::

        nao.feet.point_toes().go()
        nao.feet.right_turn_out().go()
        nao.feet.center().go()
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
    # plane
    ###################################
    def left_plane_on(self):
        """Enable balance with left foot as Plane, right foot as Fixed."""

        # stiffen body & enable wb
        self.nao.stiff()
        self.nao.whole_body_enable()

        # constrain feet
        self.nao.foot_state(self.joints.SupportLeg.RLeg, self.joints.StateName.Fixed)
        self.nao.foot_state(self.joints.SupportLeg.LLeg, self.joints.StateName.Plane)

    def right_plane_on(self):
        """Enable balance with right foot as Plane, left foot as Fixed."""

        # stiffen body & enable wb
        self.nao.stiff()
        self.nao.whole_body_enable()

        # constrain feet
        self.nao.foot_state(self.joints.SupportLeg.RLeg, self.joints.StateName.Plane)
        self.nao.foot_state(self.joints.SupportLeg.LLeg, self.joints.StateName.Fixed)

    def plane_off(self):
        """Execute queued moves, free both feet, and disable balance."""

        # block call
        self.go()

        # free feet & disable wb
        self.nao.foot_state(self.joints.SupportLeg.Legs, self.joints.StateName.Free)
        self.nao.whole_body_disable()

    ###################################
    # point
    ###################################
    def point_toes(self, duration=0, offset=0):
        """Point toes down on both feet (AnklePitch, 52.8 deg)."""
        self.left_point_toes(duration, offset)
        self.right_point_toes(duration, offset)
        return self;

    def left_point_toes(self, duration=0, offset=0):
        """Point toes down on left foot."""
        duration = self.nao.determine_duration(duration)
        angle = 52.8 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnklePitch, angle, duration)
        return self;

    def right_point_toes(self, duration=0, offset=0):
        """Point toes down on right foot."""
        duration = self.nao.determine_duration(duration)
        angle = 52.8 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnklePitch, angle, duration)
        return self;


    ###################################
    # raise
    ###################################
    def raise_toes(self, duration=0, offset=0):
        """Raise toes up on both feet (AnklePitch, -68 deg)."""
        self.right_raise_toes(duration, offset)
        self.left_raise_toes(duration, offset)
        return self;

    def right_raise_toes(self, duration=0, offset=0):
        """Raise toes up on right foot."""
        duration = self.nao.determine_duration(duration)
        angle = -68.0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnklePitch, angle, duration)
        return self;

    def left_raise_toes(self, duration=0, offset=0):
        """Raise toes up on left foot."""
        duration = self.nao.determine_duration(duration)
        angle = -68.0 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnklePitch, angle, duration)
        return self;


    ###################################
    # out
    ###################################
    def turn_out(self, duration=0, offset=0):
        """Tilt both feet outward (AnkleRoll, +/-22 deg)."""
        self.right_turn_out(duration, offset)
        self.left_turn_out(duration, offset)
        return self;

    def left_turn_out(self, duration=0, offset=0):
        """Tilt left foot outward (LAnkleRoll, 22 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 22 + offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnkleRoll, angle, duration)
        return self;

    def right_turn_out(self, duration=0, offset=0):
        """Tilt right foot outward (RAnkleRoll, -22 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = -22 - offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnkleRoll, angle, duration)
        return self;


    ###################################
    # in
    ###################################
    def turn_in(self, duration=0, offset=0):
        """Tilt both feet inward (AnkleRoll, +/-22.8 deg)."""
        self.right_turn_in(duration, offset)
        self.left_turn_in(duration, offset)
        return self;

    def left_turn_in(self, duration=0, offset=0):
        """Tilt left foot inward (LAnkleRoll, -22.8 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = -22.8 - offset
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnkleRoll, angle, duration)
        return self;

    def right_turn_in(self, duration=0, offset=0):
        """Tilt right foot inward (RAnkleRoll, 22.8 deg)."""
        duration = self.nao.determine_duration(duration)
        angle = 22.8 + offset
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnkleRoll, angle, duration)
        return self;


    ###################################
    # center
    ###################################
    def center(self, duration=0, offset=0, offset2=0):
        """Center both ankles (roll and pitch to 0)."""
        self.right_center(duration, offset, offset2)
        self.left_center(duration, offset, offset2)
        return self;

    def left_center(self, duration=0, offset=0, offset2=0):
        """Center left ankle (roll and pitch to 0)."""
        angle = 0 - offset
        angle2 = 0 - offset2

        duration = self.nao.determine_duration(duration)
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnkleRoll, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.LLeg.LAnklePitch, angle2, duration)
        return self;

    def right_center(self, duration=0, offset=0, offset2=0):
        """Center right ankle (roll and pitch to 0)."""
        duration = self.nao.determine_duration(duration)
        angle = 0 + offset
        angle2 = 0 - offset2
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnkleRoll, angle, duration)
        self.nao.move_with_degrees_and_duration(self.joints.RLeg.RAnklePitch, angle2, duration)
        return self;