'''
Created on 11 May 2014

@author: Don Najd
@description: Provider for tracking time
'''

import thread
from datetime import datetime
from time import sleep

class TimeProvider(object):

    def __init__(self, nao):

        # args
        self.nao = nao 

        # provider properties
        self.running = False
        self.subscribers = []

        # log
        self.nao.log('class=TimeProvider|method=__init__')   

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
        self.nao.log('class=TimeProvider|method=add_subscriber')  
        return self

    def setup(self):

        # tract start datetime
        self.start_datetime = datetime.now()

        # run thread
        self.running = True
        args = self,
        thread.start_new_thread(self.time_tracker, args)

        # log
        self.nao.log('class=TimeProvider|method=setup')  


    def tear_down(self):

        # stop thread
        self.running = False
        self.nao.log('class=TimeProvider|method=teardown')  


    def time_tracker(self, time_provider): 

        while time_provider.running: 

            # time elapsed
            elapsed = self.start_datetime - datetime.now()
            elapsed_sec = abs(elapsed.total_seconds())
            elapsed_min = abs(divmod(elapsed_sec, 60)[0])
            elapsed_hr = abs(divmod(elapsed_min, 60)[0])
            elapsed_days = abs(divmod(elapsed_hr, 24)[0])
            
            # callback args
            event_name = 'time_tracker'
            value = {
                'start_datetime': str(self.start_datetime), 
                'elapsed_sec': str(elapsed_sec),
                'elapsed_min': str(elapsed_min),
                'elapsed_hr': str(elapsed_hr),
                'elapsed_days': str(elapsed_days)
            }
            subscriberIdentifier = ''

            # run subscribers
            for s in self.subscribers:
                s.callback(event_name, value, subscriberIdentifier)

            # wait a second
            sleep(1) 