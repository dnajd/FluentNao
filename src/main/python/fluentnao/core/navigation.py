"""Walking, localization, and visual compass for the NAO robot.

Accessed via nao.navigation. Python 2.7 compatible.
"""

class Navigation():
    """NAO navigation using ALNavigation, ALLocalization, and ALVisualCompass.

    Uses three optional NaoQi proxies. If a proxy is unavailable, its
    methods log a warning and return self.

    Movement:
        - move_to(x, y, theta) -- precise blocking move via ALMotion.moveTo
        - navigate_to(x, y) -- obstacle-avoiding navigation via ALNavigation
        - move_toward(x, y, theta) -- continuous velocity (non-blocking)
        - stop() -- stops all movement
        - set_safety_distance(d) -- obstacle avoidance distance in meters

    Localization:
        - learn_home() / go_home() -- save and return to home position
        - go_to_position(x, y, theta) -- navigate to absolute map position
        - position() / orientation() / is_home() -- query current state
        - save_map(name) / load_map(name) / clear_map()

    Visual Compass:
        - set_compass_reference() -- capture current view as reference
        - compass_to(x, y) -- move using visual compass
        - stop_compass() -- unsubscribe from visual compass

    Notes:
        - move_to() uses ALMotion directly -- good for precise turns.
        - navigate_to() uses ALNavigation -- adds obstacle avoidance.
        - All methods return self for fluent chaining except
          position/orientation/is_home which return data or None.
    """

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log

        self.nav = self._try_proxy("ALNavigation")
        self.loc = self._try_proxy("ALLocalization")
        self.compass = self._try_proxy("ALVisualCompass")

    def _try_proxy(self, name):
        try:
            self.nao.env.add_proxy(name)
            return self.nao.env.proxies[name]
        except Exception as e:
            self.log('navigation: {} not available: {}'.format(name, e))
            return None

    ###################################
    # navigation
    ###################################

    def navigate_to(self, x, y):
        """Navigate to (x, y) with obstacle avoidance. Blocks until done."""
        if not self.nav:
            self.log('navigation.navigate_to: not available')
            return self
        self.nav.navigateTo(x, y)
        self.log('navigation.navigate_to: ({}, {})'.format(x, y))
        return self

    def move_to(self, x, y, theta=0):
        """Precise blocking move. x/y in meters, theta in radians."""
        self.nao.env.motion.moveTo(x, y, theta)
        self.log('navigation.move_to: ({}, {}, {})'.format(x, y, theta))
        return self

    def move_toward(self, x, y, theta=0):
        """Continuous velocity command (non-blocking). Call stop() to halt."""
        if not self.nav:
            self.log('navigation.move_toward: not available')
            return self
        self.nav.moveToward(x, y, theta)
        self.log('navigation.move_toward: ({}, {}, {})'.format(x, y, theta))
        return self

    def stop(self):
        """Stop all navigation and motion movement."""
        if not self.nav:
            return self
        self.nav.stopNavigateTo()
        self.nao.env.motion.stopMove()
        self.log('navigation.stop: stopped')
        return self

    def set_safety_distance(self, distance=0.4):
        """Set obstacle avoidance safety distance in meters."""
        if not self.nav:
            return self
        self.nav.setSecurityDistance(distance)
        self.log('navigation.set_safety_distance: {}'.format(distance))
        return self

    ###################################
    # localization
    ###################################

    def learn_home(self):
        """Save current position as home via panoramic scan."""
        if not self.loc:
            self.log('navigation.learn_home: not available')
            return self
        self.loc.learnHome()
        self.log('navigation.learn_home: learned current position as home')
        self.nao.say('I will remember this as home')
        return self

    def go_home(self):
        """Navigate back to learned home position."""
        if not self.loc:
            self.log('navigation.go_home: not available')
            return self
        self.loc.goToHome()
        self.log('navigation.go_home: navigating home')
        return self

    def go_to_position(self, x, y, theta=0):
        """Navigate to an absolute map position."""
        if not self.loc:
            self.log('navigation.go_to_position: not available')
            return self
        self.loc.goToPosition(x, y, theta)
        self.log('navigation.go_to_position: ({}, {}, {})'.format(x, y, theta))
        return self

    def position(self):
        """Return current robot position, or None if unavailable."""
        if not self.loc:
            return None
        try:
            return self.loc.getRobotPosition()
        except Exception:
            return None

    def orientation(self):
        """Return current robot orientation, or None if unavailable."""
        if not self.loc:
            return None
        try:
            return self.loc.getRobotOrientation()
        except Exception:
            return None

    def is_home(self):
        """Return True if robot is at home position, or None if unavailable."""
        if not self.loc:
            return None
        try:
            return self.loc.isInCurrentHome()
        except Exception:
            return None

    def save_map(self, name='map'):
        """Save the current localization map."""
        if not self.loc:
            return self
        self.loc.save(name)
        self.log('navigation.save_map: saved {}'.format(name))
        return self

    def load_map(self, name='map'):
        """Load a previously saved localization map."""
        if not self.loc:
            return self
        self.loc.load(name)
        self.log('navigation.load_map: loaded {}'.format(name))
        return self

    def clear_map(self):
        """Clear the current localization map."""
        if not self.loc:
            return self
        self.loc.clear()
        self.log('navigation.clear_map: cleared')
        return self

    ###################################
    # visual compass
    ###################################

    def set_compass_reference(self):
        """Capture current camera view as the visual compass reference."""
        if not self.compass:
            self.log('navigation.set_compass_reference: not available')
            return self
        self.compass.subscribe("fluentnao_compass")
        self.compass.setCurrentImageAsReference()
        self.log('navigation.set_compass_reference: set current view as reference')
        return self

    def compass_to(self, x, y):
        """Move to (x, y) using visual compass guidance."""
        if not self.compass:
            self.log('navigation.compass_to: not available')
            return self
        self.compass.moveTo(x, y)
        self.log('navigation.compass_to: ({}, {})'.format(x, y))
        return self

    def stop_compass(self):
        """Unsubscribe from the visual compass."""
        if not self.compass:
            return self
        try:
            self.compass.unsubscribe("fluentnao_compass")
        except Exception:
            pass
        self.log('navigation.stop_compass: stopped')
        return self
