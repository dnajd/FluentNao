"""Unified target tracking for faces, balls, landmarks, people, and sound.

Wraps the ALTracker NAOqi proxy. Accessed via nao.tracker.
"""


class Tracker():
    """Unified tracking system for any supported NAO target type.

    Supports tracking via head movement, whole body movement, or walking
    toward the target. Provides convenience methods for common targets
    and follow (walk-toward) behavior.

    Target Constants:
        FACE, RED_BALL, LANDMARK, LANDMARKS, PEOPLE, SOUND

    Mode Constants:
        HEAD       -- track using head movement only
        WHOLE_BODY -- track using head and torso
        MOVE       -- walk toward the target

    Important Notes:
        - Only one target can be tracked at a time; track() replaces the previous.
        - MOVE mode requires NAO to be standing with body stiffness enabled.
        - look_at() and point_at() use frame=0 (FRAME_TORSO) by default.
        - All chainable methods return self for fluent API usage.

    Usage Examples::

        nao.tracker.face()
        nao.tracker.face(Tracker.WHOLE_BODY)
        nao.tracker.follow_people()
        nao.tracker.track(Tracker.RED_BALL, Tracker.HEAD)
        nao.tracker.look_at(1.0, 0.0, 0.5)
        nao.tracker.stop()
    """

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
        """Register and track a target type.

        Args:
            target: Target constant (e.g. FACE, RED_BALL).
            mode: Tracking mode (HEAD, WHOLE_BODY, or MOVE). Uses current if None.
            size: Target diameter in meters (relevant for landmarks).
        """
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
        """Stop tracking and unregister all targets."""
        if not self.tracker:
            return self
        self.tracker.stopTracker()
        self.tracker.unregisterAllTargets()
        self.log('tracker.stop: stopped')
        return self

    # convenience methods
    def face(self, mode=None):
        """Track a face (defaults to HEAD mode)."""
        return self.track(self.FACE, mode or self.HEAD)

    def red_ball(self, mode=None):
        """Track a red ball (defaults to HEAD mode)."""
        return self.track(self.RED_BALL, mode or self.HEAD)

    def landmark(self, mode=None, size=0.1):
        """Track a landmark (defaults to HEAD mode)."""
        return self.track(self.LANDMARK, mode or self.HEAD, size)

    def people(self, mode=None):
        """Track people (defaults to HEAD mode)."""
        return self.track(self.PEOPLE, mode or self.HEAD)

    def sound(self, mode=None):
        """Track sound source (defaults to HEAD mode)."""
        return self.track(self.SOUND, mode or self.HEAD)

    # follow = track + walk toward
    def follow_face(self):
        """Walk toward a detected face."""
        return self.track(self.FACE, self.MOVE)

    def follow_ball(self):
        """Walk toward a red ball."""
        return self.track(self.RED_BALL, self.MOVE)

    def follow_people(self):
        """Walk toward detected people."""
        return self.track(self.PEOPLE, self.MOVE)

    def follow_sound(self):
        """Walk toward a sound source."""
        return self.track(self.SOUND, self.MOVE)

    ###################################
    # state
    ###################################

    def is_active(self):
        """Return True if tracker is currently active."""
        if not self.tracker:
            return False
        return self.tracker.isActive()

    def is_target_lost(self):
        """Return True if the current target has been lost."""
        if not self.tracker:
            return True
        return self.tracker.isTargetLost()

    def target_position(self):
        """Return target position as [x, y, z] in FRAME_TORSO, or None."""
        if not self.tracker:
            return None
        try:
            return self.tracker.getTargetPosition(0)
        except Exception:
            return None

    def active_target(self):
        """Return the name of the currently tracked target, or None."""
        if not self.tracker:
            return None
        return self.tracker.getActiveTarget()

    ###################################
    # point and look
    ###################################

    def look_at(self, x, y, z, frame=0, speed=0.5):
        """Direct NAO's gaze to a 3D point (blocking)."""
        if not self.tracker:
            return self
        self.tracker.lookAt([x, y, z], frame, speed, False)
        return self

    def point_at(self, x, y, z, frame=0, speed=0.5):
        """Point NAO's arm toward a 3D point."""
        if not self.tracker:
            return self
        self.tracker.pointAt('Arms', [x, y, z], frame, speed)
        return self

    ###################################
    # config
    ###################################

    def set_mode(self, mode):
        """Set the tracking mode (HEAD, WHOLE_BODY, or MOVE)."""
        if not self.tracker:
            return self
        self.tracker.setMode(mode)
        return self

    def set_max_distance(self, distance):
        """Set maximum detection distance in meters."""
        if not self.tracker:
            return self
        self.tracker.setMaximumDistanceDetection(distance)
        return self

    def set_timeout(self, seconds):
        """Set target-lost timeout in seconds."""
        if not self.tracker:
            return self
        self.tracker.setTimeOut(seconds)
        return self
