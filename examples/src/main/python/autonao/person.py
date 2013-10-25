
from datetime import datetime, timedelta

class Person(object):

    def __init__(self, name):

    	# args
    	self.name = name
    	self.recognize_count = 0
        self.recognize_track = []
        self.greet_count = 0
        self.greet_track = []
        
    def track_recognition(self):
    	self.recognize_count += 1
    	self.last_recognized = datetime.now()
        self.recognize_track.append(self.last_recognized)

    def track_greeting(self):
        self.greet_count += 1
        self.greet_track.append(datetime.now())

    def recog_more_than_mins(self, minutes):

        time_past = datetime.now() - self.last_recognized
        if time_past > timedelta(minutes=minutes):
            return True
        return False
