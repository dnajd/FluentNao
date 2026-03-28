import naoutil.memory as memory


class Sensors():

    # touch event names
    HEAD_FRONT = 'FrontTactilTouched'
    HEAD_MIDDLE = 'MiddleTactilTouched'
    HEAD_REAR = 'RearTactilTouched'
    BUMPER_RIGHT = 'RightBumperPressed'
    BUMPER_LEFT = 'LeftBumperPressed'
    CHEST_BUTTON = 'ChestButtonPressed'
    HAND_RIGHT = 'HandRightBackTouched'
    HAND_LEFT = 'HandLeftBackTouched'

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log
        self.body_temp = self._try_proxy("ALBodyTemperature")
        self._touch_callbacks = {}

    def _try_proxy(self, name):
        try:
            self.nao.env.add_proxy(name)
            return self.nao.env.proxies[name]
        except Exception as e:
            self.log('sensors: {} not available: {}'.format(name, e))
            return None

    ###################################
    # touch
    ###################################

    def on_touch(self, event, callback):
        self._touch_callbacks[event] = callback
        memory.subscribeToEvent(event, lambda dn, v, m: self._touch_cb(event, v))
        self.log('sensors.on_touch: subscribed to {}'.format(event))
        return self

    def stop_on_touch(self, event):
        memory.unsubscribeToEvent(event)
        self._touch_callbacks.pop(event, None)
        self.log('sensors.stop_on_touch: unsubscribed from {}'.format(event))
        return self

    def _touch_cb(self, event, value):
        cb = self._touch_callbacks.get(event)
        if cb and value == 1:
            cb(event)

    def on_head_front(self, callback):
        return self.on_touch(self.HEAD_FRONT, callback)

    def on_head_middle(self, callback):
        return self.on_touch(self.HEAD_MIDDLE, callback)

    def on_head_rear(self, callback):
        return self.on_touch(self.HEAD_REAR, callback)

    def on_head(self, callback):
        self.on_head_front(callback)
        self.on_head_middle(callback)
        self.on_head_rear(callback)
        return self

    def on_bumper_right(self, callback):
        return self.on_touch(self.BUMPER_RIGHT, callback)

    def on_bumper_left(self, callback):
        return self.on_touch(self.BUMPER_LEFT, callback)

    def on_bumper(self, callback):
        self.on_bumper_right(callback)
        self.on_bumper_left(callback)
        return self

    def on_chest_button(self, callback):
        return self.on_touch(self.CHEST_BUTTON, callback)

    def on_hand_right(self, callback):
        return self.on_touch(self.HAND_RIGHT, callback)

    def on_hand_left(self, callback):
        return self.on_touch(self.HAND_LEFT, callback)

    def on_hand(self, callback):
        self.on_hand_right(callback)
        self.on_hand_left(callback)
        return self

    def stop_all_touch(self):
        for event in list(self._touch_callbacks.keys()):
            self.stop_on_touch(event)
        return self

    ###################################
    # battery
    ###################################

    def battery_level(self):
        try:
            value = self.nao.env.memory.getData('Device/SubDeviceList/Battery/Charge/Sensor/Value')
            return int(value * 100)
        except Exception:
            return None

    def is_charging(self):
        try:
            value = self.nao.env.memory.getData('Device/SubDeviceList/Battery/Current/Sensor/Value')
            return value > 0
        except Exception:
            return None

    def battery_temperature(self):
        try:
            return self.nao.env.memory.getData('Device/SubDeviceList/Battery/Temperature/Sensor/Value')
        except Exception:
            return None

    ###################################
    # motor temperature
    ###################################

    TEMP_JOINTS = [
        'HeadYaw', 'HeadPitch',
        'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand',
        'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand',
        'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
        'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll',
    ]

    def temperatures(self):
        temps = {}
        for joint in self.TEMP_JOINTS:
            try:
                value = self.nao.env.memory.getData(
                    'Device/SubDeviceList/{}/Temperature/Sensor/Value'.format(joint))
                temps[joint] = value
            except Exception:
                pass
        return temps

    def hottest_joint(self):
        temps = self.temperatures()
        if not temps:
            return None
        joint = max(temps, key=temps.get)
        return (joint, temps[joint])

    def on_hot_joint(self, callback):
        memory.subscribeToEvent('HotJointDetected', lambda dn, v, m: callback(v))
        self.log('sensors.on_hot_joint: subscribed')
        return self

    def stop_on_hot_joint(self):
        memory.unsubscribeToEvent('HotJointDetected')
        self.log('sensors.stop_on_hot_joint: unsubscribed')
        return self
