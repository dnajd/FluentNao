import time

import naoutil.memory as memory


class People():

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log

        # proxies
        self.perception = self._try_proxy("ALPeoplePerception")
        self.engagement = self._try_proxy("ALEngagementZones")
        self.gaze = self._try_proxy("ALGazeAnalysis")
        self.sitting = self._try_proxy("ALSittingPeopleDetection")

        # callbacks
        self._on_person_arrived = None
        self._on_person_left = None
        self._on_zone1 = None
        self._on_zone2 = None
        self._on_zone3 = None
        self._on_approached = None
        self._on_moved_away = None
        self._on_looking = None
        self._on_not_looking = None
        self._on_sat_down = None
        self._on_stood_up = None

        # cooldowns
        self._last_event_times = {}

    def _try_proxy(self, name):
        try:
            self.nao.env.add_proxy(name)
            return self.nao.env.proxies[name]
        except Exception as e:
            self.log('people: {} not available: {}'.format(name, e))
            return None

    def _throttled(self, key, callback, value, cooldown=3):
        now = time.time()
        last = self._last_event_times.get(key, 0)
        if now - last > cooldown:
            self._last_event_times[key] = now
            callback(value)

    ###################################
    # people detection
    ###################################

    def on_person_arrived(self, callback):
        if not self.perception:
            self.log('people.on_person_arrived: not available')
            return self
        self._on_person_arrived = callback
        self.perception.subscribe("fluentnao_people")
        memory.subscribeToEvent('PeoplePerception/JustArrived', self._arrived_cb)
        self.log('people.on_person_arrived: subscribed')
        return self

    def stop_on_person_arrived(self):
        if not self.perception:
            return self
        memory.unsubscribeToEvent('PeoplePerception/JustArrived')
        self._on_person_arrived = None
        self.log('people.stop_on_person_arrived: unsubscribed')
        return self

    def _arrived_cb(self, dataName, value, message):
        if self._on_person_arrived and value:
            self._throttled('arrived', self._on_person_arrived, value)

    def on_person_left(self, callback):
        if not self.perception:
            self.log('people.on_person_left: not available')
            return self
        self._on_person_left = callback
        self.perception.subscribe("fluentnao_people_left")
        memory.subscribeToEvent('PeoplePerception/JustLeft', self._left_cb)
        self.log('people.on_person_left: subscribed')
        return self

    def stop_on_person_left(self):
        if not self.perception:
            return self
        memory.unsubscribeToEvent('PeoplePerception/JustLeft')
        self._on_person_left = None
        self.log('people.stop_on_person_left: unsubscribed')
        return self

    def _left_cb(self, dataName, value, message):
        if self._on_person_left and value:
            self._throttled('left', self._on_person_left, value)

    def people_count(self):
        if not self.perception:
            return 0
        try:
            people = self.nao.env.memory.getData("PeoplePerception/PeopleList")
            return len(people) if people else 0
        except Exception:
            return 0

    ###################################
    # engagement zones
    ###################################

    def on_zone1(self, callback):
        if not self.engagement:
            self.log('people.on_zone1: not available')
            return self
        self._on_zone1 = callback
        self.engagement.subscribe("fluentnao_zone1")
        memory.subscribeToEvent('EngagementZones/PersonEnteredZone1', self._zone1_cb)
        self.log('people.on_zone1: subscribed')
        return self

    def stop_on_zone1(self):
        if not self.engagement:
            return self
        memory.unsubscribeToEvent('EngagementZones/PersonEnteredZone1')
        self._on_zone1 = None
        return self

    def _zone1_cb(self, dataName, value, message):
        if self._on_zone1 and value:
            self._throttled('zone1', self._on_zone1, value)

    def on_zone2(self, callback):
        if not self.engagement:
            self.log('people.on_zone2: not available')
            return self
        self._on_zone2 = callback
        self.engagement.subscribe("fluentnao_zone2")
        memory.subscribeToEvent('EngagementZones/PersonEnteredZone2', self._zone2_cb)
        self.log('people.on_zone2: subscribed')
        return self

    def stop_on_zone2(self):
        if not self.engagement:
            return self
        memory.unsubscribeToEvent('EngagementZones/PersonEnteredZone2')
        self._on_zone2 = None
        return self

    def _zone2_cb(self, dataName, value, message):
        if self._on_zone2 and value:
            self._throttled('zone2', self._on_zone2, value)

    def on_zone3(self, callback):
        if not self.engagement:
            self.log('people.on_zone3: not available')
            return self
        self._on_zone3 = callback
        self.engagement.subscribe("fluentnao_zone3")
        memory.subscribeToEvent('EngagementZones/PersonEnteredZone3', self._zone3_cb)
        self.log('people.on_zone3: subscribed')
        return self

    def stop_on_zone3(self):
        if not self.engagement:
            return self
        memory.unsubscribeToEvent('EngagementZones/PersonEnteredZone3')
        self._on_zone3 = None
        return self

    def _zone3_cb(self, dataName, value, message):
        if self._on_zone3 and value:
            self._throttled('zone3', self._on_zone3, value)

    def on_approached(self, callback):
        if not self.engagement:
            self.log('people.on_approached: not available')
            return self
        self._on_approached = callback
        self.engagement.subscribe("fluentnao_approached")
        memory.subscribeToEvent('EngagementZones/PersonApproached', self._approached_cb)
        self.log('people.on_approached: subscribed')
        return self

    def stop_on_approached(self):
        if not self.engagement:
            return self
        memory.unsubscribeToEvent('EngagementZones/PersonApproached')
        self._on_approached = None
        return self

    def _approached_cb(self, dataName, value, message):
        if self._on_approached and value:
            self._throttled('approached', self._on_approached, value)

    def on_moved_away(self, callback):
        if not self.engagement:
            self.log('people.on_moved_away: not available')
            return self
        self._on_moved_away = callback
        self.engagement.subscribe("fluentnao_moved_away")
        memory.subscribeToEvent('EngagementZones/PersonMovedAway', self._moved_away_cb)
        self.log('people.on_moved_away: subscribed')
        return self

    def stop_on_moved_away(self):
        if not self.engagement:
            return self
        memory.unsubscribeToEvent('EngagementZones/PersonMovedAway')
        self._on_moved_away = None
        return self

    def _moved_away_cb(self, dataName, value, message):
        if self._on_moved_away and value:
            self._throttled('moved_away', self._on_moved_away, value)

    ###################################
    # gaze analysis
    ###################################

    def on_looking(self, callback):
        if not self.gaze:
            self.log('people.on_looking: not available')
            return self
        self._on_looking = callback
        self.gaze.subscribe("fluentnao_gaze")
        memory.subscribeToEvent('GazeAnalysis/PersonStartsLookingAtRobot', self._looking_cb)
        self.log('people.on_looking: subscribed')
        return self

    def stop_on_looking(self):
        if not self.gaze:
            return self
        memory.unsubscribeToEvent('GazeAnalysis/PersonStartsLookingAtRobot')
        self._on_looking = None
        return self

    def _looking_cb(self, dataName, value, message):
        if self._on_looking and value:
            self._throttled('looking', self._on_looking, value)

    def on_not_looking(self, callback):
        if not self.gaze:
            self.log('people.on_not_looking: not available')
            return self
        self._on_not_looking = callback
        self.gaze.subscribe("fluentnao_gaze_stop")
        memory.subscribeToEvent('GazeAnalysis/PersonStopsLookingAtRobot', self._not_looking_cb)
        self.log('people.on_not_looking: subscribed')
        return self

    def stop_on_not_looking(self):
        if not self.gaze:
            return self
        memory.unsubscribeToEvent('GazeAnalysis/PersonStopsLookingAtRobot')
        self._on_not_looking = None
        return self

    def _not_looking_cb(self, dataName, value, message):
        if self._on_not_looking and value:
            self._throttled('not_looking', self._on_not_looking, value)

    ###################################
    # sitting detection
    ###################################

    def on_sat_down(self, callback):
        if not self.sitting:
            self.log('people.on_sat_down: not available')
            return self
        self._on_sat_down = callback
        self.sitting.subscribe("fluentnao_sitting")
        memory.subscribeToEvent('SittingPeopleDetection/PersonSittingDown', self._sat_down_cb)
        self.log('people.on_sat_down: subscribed')
        return self

    def stop_on_sat_down(self):
        if not self.sitting:
            return self
        memory.unsubscribeToEvent('SittingPeopleDetection/PersonSittingDown')
        self._on_sat_down = None
        return self

    def _sat_down_cb(self, dataName, value, message):
        if self._on_sat_down and value:
            self._throttled('sat_down', self._on_sat_down, value)

    def on_stood_up(self, callback):
        if not self.sitting:
            self.log('people.on_stood_up: not available')
            return self
        self._on_stood_up = callback
        self.sitting.subscribe("fluentnao_stood_up")
        memory.subscribeToEvent('SittingPeopleDetection/PersonStandingUp', self._stood_up_cb)
        self.log('people.on_stood_up: subscribed')
        return self

    def stop_on_stood_up(self):
        if not self.sitting:
            return self
        memory.unsubscribeToEvent('SittingPeopleDetection/PersonStandingUp')
        self._on_stood_up = None
        return self

    def _stood_up_cb(self, dataName, value, message):
        if self._on_stood_up and value:
            self._throttled('stood_up', self._on_stood_up, value)

    ###################################
    # stop all
    ###################################

    def stop_all(self):
        self.stop_on_person_arrived()
        self.stop_on_person_left()
        self.stop_on_zone1()
        self.stop_on_zone2()
        self.stop_on_zone3()
        self.stop_on_approached()
        self.stop_on_moved_away()
        self.stop_on_looking()
        self.stop_on_not_looking()
        self.stop_on_sat_down()
        self.stop_on_stood_up()
        self.log('people.stop_all: all unsubscribed')
        return self
