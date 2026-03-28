"""
Navigation module for NAO robot walking, localization, and visual compass.

Python 2.7 compatible. Accessed via nao.navigation (instance of Navigation class).
Uses three optional NaoQi proxies: ALNavigation, ALLocalization, ALVisualCompass.
If a proxy is unavailable, its methods log a warning and return self.

Movement
--------
  - move_to(x, y, theta=0)        -- precise movement using ALMotion.moveTo directly.
                                      x/y in meters, theta in radians. Accurate for turns.
                                      Blocks until movement completes.
  - navigate_to(x, y)             -- obstacle-avoiding navigation using ALNavigation.navigateTo.
                                      Blocks until destination reached or path fails.
  - move_toward(x, y, theta=0)    -- continuous velocity command via ALNavigation.moveToward.
                                      Does not block; call stop() to halt.
  - stop()                        -- stops both ALNavigation and ALMotion movement.
  - set_safety_distance(d=0.4)    -- sets obstacle avoidance safety distance in meters.

Localization
------------
  - learn_home()                   -- performs panoramic scan and saves current position as home.
  - go_home()                      -- navigates back to learned home position.
  - go_to_position(x, y, theta=0) -- navigates to an absolute map position.
  - position()                     -- returns current [x, y, theta] from ALLocalization, or None.
  - orientation()                  -- returns current orientation, or None.
  - is_home()                      -- returns True if robot is near home, or None.
  - save_map(name='map')           -- persists the learned map.
  - load_map(name='map')           -- loads a previously saved map.
  - clear_map()                    -- clears the current map.

Visual Compass
--------------
  - set_compass_reference()        -- captures current camera image as compass reference.
  - compass_to(x, y)              -- moves toward a position using visual compass.
  - stop_compass()                 -- unsubscribes from the visual compass.

Usage Examples
--------------
    # Walk forward 1 meter
    nao.navigation.move_to(1.0, 0, 0)

    # Turn 90 degrees left in place
    import math
    nao.navigation.move_to(0, 0, math.pi / 2)

    # Navigate with obstacle avoidance
    nao.navigation.navigate_to(2.0, 1.0)

    # Learn and return to home
    nao.navigation.learn_home()
    # ... robot walks around ...
    nao.navigation.go_home()

Notes
-----
- move_to() uses ALMotion directly -- good for precise turns and short distances.
- navigate_to() uses ALNavigation -- adds obstacle avoidance but may be less precise.
- All methods return self for fluent chaining (except position/orientation/is_home
  which return data or None).
"""

class Navigation():

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
        if not self.nav:
            self.log('navigation.navigate_to: not available')
            return self
        self.nav.navigateTo(x, y)
        self.log('navigation.navigate_to: ({}, {})'.format(x, y))
        return self

    def move_to(self, x, y, theta=0):
        self.nao.env.motion.moveTo(x, y, theta)
        self.log('navigation.move_to: ({}, {}, {})'.format(x, y, theta))
        return self

    def move_toward(self, x, y, theta=0):
        if not self.nav:
            self.log('navigation.move_toward: not available')
            return self
        self.nav.moveToward(x, y, theta)
        self.log('navigation.move_toward: ({}, {}, {})'.format(x, y, theta))
        return self

    def stop(self):
        if not self.nav:
            return self
        self.nav.stopNavigateTo()
        self.nao.env.motion.stopMove()
        self.log('navigation.stop: stopped')
        return self

    def set_safety_distance(self, distance=0.4):
        if not self.nav:
            return self
        self.nav.setSecurityDistance(distance)
        self.log('navigation.set_safety_distance: {}'.format(distance))
        return self

    ###################################
    # localization
    ###################################

    def learn_home(self):
        if not self.loc:
            self.log('navigation.learn_home: not available')
            return self
        self.loc.learnHome()
        self.log('navigation.learn_home: learned current position as home')
        self.nao.say('I will remember this as home')
        return self

    def go_home(self):
        if not self.loc:
            self.log('navigation.go_home: not available')
            return self
        self.loc.goToHome()
        self.log('navigation.go_home: navigating home')
        return self

    def go_to_position(self, x, y, theta=0):
        if not self.loc:
            self.log('navigation.go_to_position: not available')
            return self
        self.loc.goToPosition(x, y, theta)
        self.log('navigation.go_to_position: ({}, {}, {})'.format(x, y, theta))
        return self

    def position(self):
        if not self.loc:
            return None
        try:
            return self.loc.getRobotPosition()
        except Exception:
            return None

    def orientation(self):
        if not self.loc:
            return None
        try:
            return self.loc.getRobotOrientation()
        except Exception:
            return None

    def is_home(self):
        if not self.loc:
            return None
        try:
            return self.loc.isInCurrentHome()
        except Exception:
            return None

    def save_map(self, name='map'):
        if not self.loc:
            return self
        self.loc.save(name)
        self.log('navigation.save_map: saved {}'.format(name))
        return self

    def load_map(self, name='map'):
        if not self.loc:
            return self
        self.loc.load(name)
        self.log('navigation.load_map: loaded {}'.format(name))
        return self

    def clear_map(self):
        if not self.loc:
            return self
        self.loc.clear()
        self.log('navigation.clear_map: cleared')
        return self

    ###################################
    # visual compass
    ###################################

    def set_compass_reference(self):
        if not self.compass:
            self.log('navigation.set_compass_reference: not available')
            return self
        self.compass.subscribe("fluentnao_compass")
        self.compass.setCurrentImageAsReference()
        self.log('navigation.set_compass_reference: set current view as reference')
        return self

    def compass_to(self, x, y):
        if not self.compass:
            self.log('navigation.compass_to: not available')
            return self
        self.compass.moveTo(x, y)
        self.log('navigation.compass_to: ({}, {})'.format(x, y))
        return self

    def stop_compass(self):
        if not self.compass:
            return self
        try:
            self.compass.unsubscribe("fluentnao_compass")
        except Exception:
            pass
        self.log('navigation.stop_compass: stopped')
        return self
