"""NAO robot event name constants, grouped by category.

Accessed via nao.events (instance of Events class). Each category is an
Enum-like set where attributes return the event name string.

Usage:
    nao.events.touch.FrontTactilTouched    # 'FrontTactilTouched'
    nao.events.vision.FaceDetected         # 'FaceDetected'
    nao.events.people.PersonEnteredZone1   # 'EngagementZones/PersonEnteredZone1'

    # Subscribe using the constant
    memory.subscribeToEvent(nao.events.touch.ChestButtonPressed, callback)

    # Iterate all events in a category
    for event in nao.events.touch:
        print(event)

Categories:
    touch    -- head tactile, foot bumpers, hand sensors, chest button
    vision   -- face, ball, object, landmark, movement, darkness detection
    people   -- arrival/departure, zones, gaze, sitting
    audio    -- speech recognition, sound detection, sound localization
    sensors  -- hot joints, battery, sonar
    nav      -- obstacle detection
"""


class _Enum(set):
    """Set subclass that allows attribute access to members."""
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError(name)


class Events():
    """All NAO robot events grouped by category.

    Each category is an _Enum (set with attribute access).

    Categories:
        events.touch   -- touch/button events (fire with value 1 on press)
        events.vision  -- visual detection events
        events.people  -- people perception, zones, gaze, sitting
        events.audio   -- speech and sound events
        events.sensors -- hardware alerts (temperature, battery, sonar)
        events.nav     -- navigation/obstacle events
    """

    def __init__(self):
        self.touch = _Enum([
            # head tactile sensors
            'FrontTactilTouched',
            'MiddleTactilTouched',
            'RearTactilTouched',
            # foot bumpers
            'LeftBumperPressed',
            'RightBumperPressed',
            # chest
            'ChestButtonPressed',
            # hand sensors
            'HandLeftBackTouched',
            'HandLeftLeftTouched',
            'HandLeftRightTouched',
            'HandRightBackTouched',
            'HandRightLeftTouched',
            'HandRightRightTouched',
        ])

        self.vision = _Enum([
            # face
            'FaceDetected',
            # red ball
            'redBallDetected',
            # object/picture recognition
            'PictureDetected',
            # landmarks (NAOmarks)
            'LandmarkDetected',
            # movement
            'MovementDetection/MovementDetected',
            'MovementDetection/NoMovement',
            # darkness
            'DarknessDetection/DarknessDetected',
            # backlighting
            'BacklightingDetection/BacklightingDetected',
        ])

        self.people = _Enum([
            # arrival/departure
            'PeoplePerception/JustArrived',
            'PeoplePerception/JustLeft',
            'PeoplePerception/PeopleDetected',
            # engagement zones
            'EngagementZones/PersonEnteredZone1',
            'EngagementZones/PersonEnteredZone2',
            'EngagementZones/PersonEnteredZone3',
            'EngagementZones/PersonApproached',
            'EngagementZones/PersonMovedAway',
            # gaze
            'GazeAnalysis/PersonStartsLookingAtRobot',
            'GazeAnalysis/PersonStopsLookingAtRobot',
            # sitting
            'SittingPeopleDetection/PersonSittingDown',
            'SittingPeopleDetection/PersonStandingUp',
        ])

        self.audio = _Enum([
            # speech recognition
            'WordRecognized',
            # sound detection
            'SoundDetected',
            'SpeechDetected',
            # sound localization
            'ALAudioSourceLocalization/SoundLocated',
        ])

        self.sensors = _Enum([
            # temperature
            'HotJointDetected',
            'DeviceNoLongerHotDetected',
            # battery
            'BatteryChargeChanged',
            'BatteryLowDetected',
            'BatteryEmpty',
            'BatteryChargingFlagChanged',
            'BatteryPowerPluggedChanged',
            # sonar
            'SonarLeftDetected',
            'SonarRightDetected',
            'SonarLeftNothingDetected',
            'SonarRightNothingDetected',
        ])

        self.nav = _Enum([
            'Navigation/AvoidanceNavigator/ObstacleDetected',
            'Navigation/SafeNavigator/DangerousObstacleDetected',
        ])

    def all(self):
        """Return a flat list of all event names across all categories."""
        result = []
        for category in [self.touch, self.vision, self.people,
                         self.audio, self.sensors, self.nav]:
            result.extend(sorted(category))
        return result
