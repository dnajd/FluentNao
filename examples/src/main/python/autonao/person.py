
from datetime import datetime, timedelta

class Person(object):

    def __init__(self, name):

    	# args
    	self.name = name
    	self.recognize_count = 0
    	
    	
    def track_recognition(self):

    	# recognize
    	self.recognize_count += 1
    	self.last_recognized = datetime.now()

    def recog_more_than_mins(self, minutes):

        time_past = datetime.now() - lself.last_recognized
        if time_past > timedelta(minutes=minutes):
            return true
        return false
