"""
Tracker module -- unified tracking system for NAO robot that can track any
supported target type using head movement, whole body movement, or walking.

This module provides the Tracker class, accessed via nao.tracker, which wraps
the ALTracker NAOqi proxy. It provides a single consistent API for tracking
faces, red balls, landmarks, people, and sound sources.

Target Constants:
    Tracker.FACE      = 'Face'
    Tracker.RED_BALL  = 'RedBall'
    Tracker.LANDMARK  = 'LandMark'
    Tracker.LANDMARKS = 'LandMarks'
    Tracker.PEOPLE    = 'People'
    Tracker.SOUND     = 'Sound'

Mode Constants:
    Tracker.HEAD       = 'Head'       -- track using head movement only
    Tracker.WHOLE_BODY = 'WholeBody'  -- track using head and torso
    Tracker.MOVE       = 'Move'       -- walk toward the target

Key Methods -- Tracking:
    track(target, mode=None, size=0.1)
        Register and track any target type. If mode is provided, sets the
        tracking mode first. The size parameter is the target's physical
        diameter in meters (relevant for landmarks). Returns self.

    stop()
        Stop tracking, unregister all targets. Returns self.

Key Methods -- Convenience (default to HEAD mode):
    face(mode=None)       -- track a face
    red_ball(mode=None)   -- track a red ball
    landmark(mode=None, size=0.1) -- track a landmark
    people(mode=None)     -- track people
    sound(mode=None)      -- track sound source

Key Methods -- Follow (uses MOVE mode, NAO walks toward target):
    follow_face()         -- walk toward detected face
    follow_ball()         -- walk toward red ball
    follow_people()       -- walk toward people
    follow_sound()        -- walk toward sound source

Key Methods -- Point and Look:
    look_at(x, y, z, frame=0, speed=0.5)
        Direct NAO's gaze to a 3D point. frame=0 is FRAME_TORSO.
        Blocking call. Returns self.

    point_at(x, y, z, frame=0, speed=0.5)
        Point NAO's arm toward a 3D point. Uses 'Arms' effector.
        Returns self.

Key Methods -- State:
    is_active()
        Returns True if tracker is currently active.

    is_target_lost()
        Returns True if the current target has been lost.

    target_position()
        Returns the current target position as [x, y, z] in FRAME_TORSO,
        or None if unavailable.

    active_target()
        Returns the name of the currently tracked target, or None.

Key Methods -- Configuration:
    set_mode(mode)
        Set the tracking mode (HEAD, WHOLE_BODY, or MOVE). Returns self.

    set_max_distance(distance)
        Set maximum detection distance in meters. Returns self.

    set_timeout(seconds)
        Set target-lost timeout in seconds. Returns self.

Usage Examples:
    # Track a face with head only
    nao.tracker.face()

    # Track a face with whole body
    nao.tracker.face(Tracker.WHOLE_BODY)

    # Follow a person (walk toward them)
    nao.tracker.follow_people()

    # Generic tracking
    nao.tracker.track(Tracker.RED_BALL, Tracker.HEAD)

    # Check state
    if not nao.tracker.is_target_lost():
        pos = nao.tracker.target_position()

    # Look at a specific point
    nao.tracker.look_at(1.0, 0.0, 0.5)

    # Stop all tracking
    nao.tracker.stop()

Important Notes:
    - Only one target can be tracked at a time; calling track() replaces the
      previous target.
    - MOVE mode requires NAO to be standing and have body stiffness enabled.
    - look_at() and point_at() use frame=0 (FRAME_TORSO) by default.
    - Unavailable proxies are handled gracefully (methods log and return self).
    - All chainable methods return self for fluent API usage.
    - This is Python 2.7 code.
"""


class Tracker():

    # modes
    HEAD = 'Head'
    WHOLE_BODY = 'WholeBody'
    MOVE = 'Move'

    # targets
    FACE = 'Face'
    RED_BALL = 'RedBall'
    LANDMARK = 'LandMark'
    LANDMARKS = 'LandMarks'
    PEOPLE = 'People'
    SOUND = 'Sound'

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log
        self.tracker = self._try_proxy("ALTracker")

    def _try_proxy(self, name):
        try:
            self.nao.env.add_proxy(name)
            return self.nao.env.proxies[name]
        except Exception as e:
            self.log('tracker: {} not available: {}'.format(name, e))
            return None

    ###################################
    # tracking
    ###################################

    def track(self, target, mode=None, size=0.1):
        if not self.tracker:
            self.log('tracker.track: not available')
            return self
        if mode:
            self.tracker.setMode(mode)
        self.tracker.registerTarget(target, size)
        self.tracker.track(target)
        self.log('tracker.track: {} mode={}'.format(target, mode or self.tracker.getMode()))
        return self

    def stop(self):
        if not self.tracker:
            return self
        self.tracker.stopTracker()
        self.tracker.unregisterAllTargets()
        self.log('tracker.stop: stopped')
        return self

    # convenience methods
    def face(self, mode=None):
        return self.track(self.FACE, mode or self.HEAD)

    def red_ball(self, mode=None):
        return self.track(self.RED_BALL, mode or self.HEAD)

    def landmark(self, mode=None, size=0.1):
        return self.track(self.LANDMARK, mode or self.HEAD, size)

    def people(self, mode=None):
        return self.track(self.PEOPLE, mode or self.HEAD)

    def sound(self, mode=None):
        return self.track(self.SOUND, mode or self.HEAD)

    # follow = track + walk toward
    def follow_face(self):
        return self.track(self.FACE, self.MOVE)

    def follow_ball(self):
        return self.track(self.RED_BALL, self.MOVE)

    def follow_people(self):
        return self.track(self.PEOPLE, self.MOVE)

    def follow_sound(self):
        return self.track(self.SOUND, self.MOVE)

    ###################################
    # state
    ###################################

    def is_active(self):
        if not self.tracker:
            return False
        return self.tracker.isActive()

    def is_target_lost(self):
        if not self.tracker:
            return True
        return self.tracker.isTargetLost()

    def target_position(self):
        if not self.tracker:
            return None
        try:
            return self.tracker.getTargetPosition(0)
        except Exception:
            return None

    def active_target(self):
        if not self.tracker:
            return None
        return self.tracker.getActiveTarget()

    ###################################
    # point and look
    ###################################

    def look_at(self, x, y, z, frame=0, speed=0.5):
        if not self.tracker:
            return self
        self.tracker.lookAt([x, y, z], frame, speed, False)
        return self

    def point_at(self, x, y, z, frame=0, speed=0.5):
        if not self.tracker:
            return self
        self.tracker.pointAt('Arms', [x, y, z], frame, speed)
        return self

    ###################################
    # config
    ###################################

    def set_mode(self, mode):
        if not self.tracker:
            return self
        self.tracker.setMode(mode)
        return self

    def set_max_distance(self, distance):
        if not self.tracker:
            return self
        self.tracker.setMaximumDistanceDetection(distance)
        return self

    def set_timeout(self, seconds):
        if not self.tracker:
            return self
        self.tracker.setTimeOut(seconds)
        return self
