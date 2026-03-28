"""Touch events, battery status, and motor temperature for the NAO robot.

Accessed via nao.sensors. Python 2.7 compatible.
"""
import naoutil.memory as memory


class Sensors():
    """NAO sensor interface for touch events, battery, and motor temperatures.

    Touch Events:
        Register callbacks that fire when a sensor is touched (value == 1 only).
        All touch methods return self for chaining. Callbacks receive one
        argument: the event name string (e.g. 'FrontTactilTouched').

        - on_head(cb) -- subscribes to all three head tactile sensors
        - on_head_front(cb), on_head_middle(cb), on_head_rear(cb)
        - on_bumper(cb) -- subscribes to both foot bumpers
        - on_bumper_left(cb), on_bumper_right(cb)
        - on_chest_button(cb), on_hand(cb), on_hand_left(cb), on_hand_right(cb)
        - stop_on_touch(event) / stop_all_touch()

    Battery:
        - battery_level() -- returns 0-100 (int) or None on error
        - is_charging() -- returns True/False or None on error
        - battery_temperature() -- returns temperature value or None

    Motor Temperature:
        - temperatures() -- dict of all 26 joint names to temperature values
        - hottest_joint() -- (joint_name, temperature) tuple or None
        - on_hot_joint(cb) / stop_on_hot_joint()

    Notes:
        - Touch callbacks only fire on press (value == 1), not release.
        - ALBodyTemperature proxy is optional; if unavailable, temp methods
          log a warning.
        - All methods return self where possible for fluent chaining.
    """

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log
        self.body_temp = self._try_proxy("ALBodyTemperature")
        self._touch_callbacks = {}

        # touch event names from events module
        e = nao.events.touch
        self.HEAD_FRONT = e.FrontTactilTouched
        self.HEAD_MIDDLE = e.MiddleTactilTouched
        self.HEAD_REAR = e.RearTactilTouched
        self.BUMPER_RIGHT = e.RightBumperPressed
        self.BUMPER_LEFT = e.LeftBumperPressed
        self.CHEST_BUTTON = e.ChestButtonPressed
        self.HAND_RIGHT = e.HandRightBackTouched
        self.HAND_LEFT = e.HandLeftBackTouched

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
        """Subscribe to a touch event with a callback."""
        self._touch_callbacks[event] = callback
        memory.subscribeToEvent(event, lambda dn, v, m: self._touch_cb(event, v))
        self.log('sensors.on_touch: subscribed to {}'.format(event))
        return self

    def stop_on_touch(self, event):
        """Unsubscribe from a specific touch event."""
        memory.unsubscribeToEvent(event)
        self._touch_callbacks.pop(event, None)
        self.log('sensors.stop_on_touch: unsubscribed from {}'.format(event))
        return self

    def _touch_cb(self, event, value):
        cb = self._touch_callbacks.get(event)
        if cb and value == 1:
            cb(event)

    def on_head_front(self, callback):
        """Subscribe to front head tactile sensor."""
        return self.on_touch(self.HEAD_FRONT, callback)

    def on_head_middle(self, callback):
        """Subscribe to middle head tactile sensor."""
        return self.on_touch(self.HEAD_MIDDLE, callback)

    def on_head_rear(self, callback):
        """Subscribe to rear head tactile sensor."""
        return self.on_touch(self.HEAD_REAR, callback)

    def on_head(self, callback):
        """Subscribe to all three head tactile sensors."""
        self.on_head_front(callback)
        self.on_head_middle(callback)
        self.on_head_rear(callback)
        return self

    def on_bumper_right(self, callback):
        """Subscribe to right foot bumper."""
        return self.on_touch(self.BUMPER_RIGHT, callback)

    def on_bumper_left(self, callback):
        """Subscribe to left foot bumper."""
        return self.on_touch(self.BUMPER_LEFT, callback)

    def on_bumper(self, callback):
        """Subscribe to both foot bumpers."""
        self.on_bumper_right(callback)
        self.on_bumper_left(callback)
        return self

    def on_chest_button(self, callback):
        """Subscribe to chest button press."""
        return self.on_touch(self.CHEST_BUTTON, callback)

    def on_hand_right(self, callback):
        """Subscribe to right hand back sensor."""
        return self.on_touch(self.HAND_RIGHT, callback)

    def on_hand_left(self, callback):
        """Subscribe to left hand back sensor."""
        return self.on_touch(self.HAND_LEFT, callback)

    def on_hand(self, callback):
        """Subscribe to both hand back sensors."""
        self.on_hand_right(callback)
        self.on_hand_left(callback)
        return self

    def stop_all_touch(self):
        """Unsubscribe from all registered touch events."""
        for event in list(self._touch_callbacks.keys()):
            self.stop_on_touch(event)
        return self

    ###################################
    # battery
    ###################################

    def battery_level(self):
        """Return battery charge as 0-100 int, or None on error."""
        try:
            value = self.nao.env.memory.getData('Device/SubDeviceList/Battery/Charge/Sensor/Value')
            return int(value * 100)
        except Exception:
            return None

    def is_charging(self):
        """Return True if charging, False if not, None on error."""
        try:
            value = self.nao.env.memory.getData('Device/SubDeviceList/Battery/Current/Sensor/Value')
            return value > 0
        except Exception:
            return None

    def battery_temperature(self):
        """Return battery temperature value, or None on error."""
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
        """Return dict mapping all 26 joint names to their temperatures."""
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
        """Return (joint_name, temperature) for the hottest joint, or None."""
        temps = self.temperatures()
        if not temps:
            return None
        joint = max(temps, key=temps.get)
        return (joint, temps[joint])

    def on_hot_joint(self, callback):
        """Subscribe to HotJointDetected event."""
        memory.subscribeToEvent(self.nao.events.sensors.HotJointDetected, lambda dn, v, m: callback(v))
        self.log('sensors.on_hot_joint: subscribed')
        return self

    def stop_on_hot_joint(self):
        """Unsubscribe from HotJointDetected event."""
        memory.unsubscribeToEvent(self.nao.events.sensors.HotJointDetected)
        self.log('sensors.stop_on_hot_joint: unsubscribed')
        return self
