'''
Created on 20 May 2014

@author: Don Najd
@description: Provider for Naoqi Face Recognition
'''

from datetime import datetime, timedelta

class FaceRecogProvider(object):

    def __init__(self, nao, memory):

        # args
        self.nao = nao 
        self.memory = memory

        # provider properties
        self.running = False
        self.subscribers = []
        self.logged_recog = {}

        # facetracker
        self.nao.env.add_proxy("ALFaceTracker")   
        self.facetracker = self.nao.env.proxies["ALFaceTracker"] 

        # log
        self.nao.log('class=FaceRecogProvider|method=__init__')   

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
        self.nao.log('class=FaceRecogProvider|method=add_subscriber')  
        return self

    def setup(self):
        self.memory.subscribeToEvent('FaceDetected', self.event_callback)
        self.nao.log('class=FaceRecogProvider|method=setup')  

        # face track
        self.nao.env.motion.setStiffnesses("Head", 1.0)


    def tear_down(self):
        self.memory.unsubscribeToEvent('FaceDetected')
        self.nao.log('class=FaceRecogProvider|method=teardown')  

        # face track
        self.nao.env.motion.setStiffnesses("Head", 0)

    def event_callback(self, naoqi_dataName, naoqi_value, naoqi_message): 
      
        # status
        self.running = True
        #self.nao.log('class=FaceRecogProvider|method=event_callback|action=call_subscribers')  
        
        # get nane
        try:
            name = naoqi_value[1][1][1][0]    # get name from naoqi
        except IndexError:
            name = ''

        # callback args
        event_name = 'face_recog'
        value = {
            'name': name
        }
        subscriberIdentifier = ''

        # get person
        person = None
        if len(name) > 0:
            self.nao.log('class=FaceRecogProvider|method=event_callback|name=' + name)

            # person
            if not name in self.logged_recog:
                person = Person(name)
                self.logged_recog[name] = person

            else:
                person = self.logged_recog[name]
            
            # track
            person.count_this_recognition()

            # add to callback args
            value['person'] = person

        # call subscribers
        for s in self.subscribers:
            s.callback(event_name, value, subscriberIdentifier)

        self.running = False 

# Tracking
class Person(object):

    def __init__(self, name):

        # args
        self.name = name
        self.recognize_count = 0
        self.recognize_track = []
        self.greet_count = 0
        self.greet_track = []
        
    def count_this_recognition(self):
        self.recognize_count += 1
        self.last_recognized = datetime.now()
        self.recognize_track.append(self.last_recognized)

    def count_this_greeting(self):
        self.greet_count += 1
        self.greet_track.append(datetime.now())

    def recog_more_than_mins(self, minutes):

        time_past = datetime.now() - self.last_recognized
        if time_past > timedelta(minutes=minutes):
            return True
        return False