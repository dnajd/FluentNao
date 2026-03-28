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
