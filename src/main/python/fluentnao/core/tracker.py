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
