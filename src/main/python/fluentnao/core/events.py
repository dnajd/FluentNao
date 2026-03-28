"""NAO robot event name constants, grouped by category.

Accessed via nao.events. Each category maps clean attribute names
to the full NAOqi event strings (which may contain slashes).

Usage:
    nao.events.touch.FrontTactilTouched       # 'FrontTactilTouched'
    nao.events.vision.FaceDetected            # 'FaceDetected'
    nao.events.people.JustArrived             # 'PeoplePerception/JustArrived'
    nao.events.people.PersonEnteredZone1      # 'EngagementZones/PersonEnteredZone1'

    # Subscribe using the constant
    memory.subscribeToEvent(nao.events.touch.ChestButtonPressed, callback)

    # Iterate all events in a category
    for name, event_string in nao.events.touch.items():
        print(name, event_string)

Categories:
    touch    -- head tactile, foot bumpers, hand sensors, chest button
    vision   -- face, ball, object, landmark, movement, darkness detection
    people   -- arrival/departure, zones, gaze, sitting
    audio    -- speech recognition, sound detection, sound localization
    sensors  -- hot joints, battery, sonar
    nav      -- obstacle detection
"""


class _EventGroup(object):
    """Dict-like object where attributes return event name strings.

    Supports attribute access, iteration, len(), and 'in' operator.
    Attribute names are clean Python identifiers that map to the full
    NAOqi event string (which may contain slashes).
    """

    def __init__(self, mapping):
        object.__setattr__(self, '_mapping', mapping)

    def __getattr__(self, name):
        mapping = object.__getattribute__(self, '_mapping')
        if name in mapping:
            return mapping[name]
        raise AttributeError(name)

    def __iter__(self):
        return iter(object.__getattribute__(self, '_mapping').values())

    def __len__(self):
        return len(object.__getattribute__(self, '_mapping'))

    def __contains__(self, item):
        return item in object.__getattribute__(self, '_mapping').values()

    def items(self):
        """Return (attr_name, event_string) pairs."""
        return object.__getattribute__(self, '_mapping').items()

    def values(self):
        """Return all event strings."""
        return object.__getattribute__(self, '_mapping').values()

    def keys(self):
        """Return all attribute names."""
        return object.__getattribute__(self, '_mapping').keys()


class Events():
    """All NAO robot events grouped by category.

    Each category is an _EventGroup where attributes map clean names
    to the full NAOqi event strings.

    Categories:
        events.touch   -- touch/button events (fire with value 1 on press)
        events.vision  -- visual detection events
        events.people  -- people perception, zones, gaze, sitting
        events.audio   -- speech and sound events
        events.sensors -- hardware alerts (temperature, battery, sonar)
        events.nav     -- navigation/obstacle events
    """

    def __init__(self):
        self.touch = _EventGroup({
            # head tactile sensors
            'FrontTactilTouched': 'FrontTactilTouched',
            'MiddleTactilTouched': 'MiddleTactilTouched',
            'RearTactilTouched': 'RearTactilTouched',
            # foot bumpers
            'LeftBumperPressed': 'LeftBumperPressed',
            'RightBumperPressed': 'RightBumperPressed',
            # chest
            'ChestButtonPressed': 'ChestButtonPressed',
            # hand sensors
            'HandLeftBackTouched': 'HandLeftBackTouched',
            'HandLeftLeftTouched': 'HandLeftLeftTouched',
            'HandLeftRightTouched': 'HandLeftRightTouched',
            'HandRightBackTouched': 'HandRightBackTouched',
            'HandRightLeftTouched': 'HandRightLeftTouched',
            'HandRightRightTouched': 'HandRightRightTouched',
        })

        self.vision = _EventGroup({
            'FaceDetected': 'FaceDetected',
            'redBallDetected': 'redBallDetected',
            'PictureDetected': 'PictureDetected',
            'LandmarkDetected': 'LandmarkDetected',
            'MovementDetected': 'MovementDetection/MovementDetected',
            'NoMovement': 'MovementDetection/NoMovement',
            'DarknessDetected': 'DarknessDetection/DarknessDetected',
            'BacklightingDetected': 'BacklightingDetection/BacklightingDetected',
        })

        self.people = _EventGroup({
            'JustArrived': 'PeoplePerception/JustArrived',
            'JustLeft': 'PeoplePerception/JustLeft',
            'PeopleDetected': 'PeoplePerception/PeopleDetected',
            'PersonEnteredZone1': 'EngagementZones/PersonEnteredZone1',
            'PersonEnteredZone2': 'EngagementZones/PersonEnteredZone2',
            'PersonEnteredZone3': 'EngagementZones/PersonEnteredZone3',
            'PersonApproached': 'EngagementZones/PersonApproached',
            'PersonMovedAway': 'EngagementZones/PersonMovedAway',
            'StartedLooking': 'GazeAnalysis/PersonStartsLookingAtRobot',
            'StoppedLooking': 'GazeAnalysis/PersonStopsLookingAtRobot',
            'PersonSatDown': 'SittingPeopleDetection/PersonSittingDown',
            'PersonStoodUp': 'SittingPeopleDetection/PersonStandingUp',
        })

        self.audio = _EventGroup({
            'WordRecognized': 'WordRecognized',
            'SoundDetected': 'SoundDetected',
            'SpeechDetected': 'SpeechDetected',
            'SoundLocated': 'ALAudioSourceLocalization/SoundLocated',
        })

        self.sensors = _EventGroup({
            'HotJointDetected': 'HotJointDetected',
            'DeviceNoLongerHot': 'DeviceNoLongerHotDetected',
            'BatteryChargeChanged': 'BatteryChargeChanged',
            'BatteryLowDetected': 'BatteryLowDetected',
            'BatteryEmpty': 'BatteryEmpty',
            'BatteryChargingChanged': 'BatteryChargingFlagChanged',
            'BatteryPluggedChanged': 'BatteryPowerPluggedChanged',
            'SonarLeftDetected': 'SonarLeftDetected',
            'SonarRightDetected': 'SonarRightDetected',
            'SonarLeftNothing': 'SonarLeftNothingDetected',
            'SonarRightNothing': 'SonarRightNothingDetected',
        })

        self.nav = _EventGroup({
            'ObstacleDetected': 'Navigation/AvoidanceNavigator/ObstacleDetected',
            'DangerousObstacle': 'Navigation/SafeNavigator/DangerousObstacleDetected',
        })

    def all(self):
        """Return a flat list of all event name strings across all categories."""
        result = []
        for category in [self.touch, self.vision, self.people,
                         self.audio, self.sensors, self.nav]:
            result.extend(category)
        return result
