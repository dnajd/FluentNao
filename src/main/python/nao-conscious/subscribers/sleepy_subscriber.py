'''
Created on 17 May 2014

@author: Don Najd
@description: Nao will get sleepy after a while
'''
import random

class SleepySubscriber(object):

    def __init__(self, nao):

        self.nao = nao 
        self.nao.log('class=SleepySubscriber|method=__init__')

    def callback(self, eventName, value, subscriberIdentifier):

        if eventName == 'time_tracker':

            # time elapsed in sec
            #start_datetime = value['start_datetime']
            elapsed_sec = round(float(value['elapsed_sec']))

            
            if elapsed_sec == 10.0:
                self.nao.sit_say('Think_3', 'its good to be alive')
                self.nao.log('class=SleepySubscriber|method=callback|action=wake|elapsed_sec=' + str(elapsed_sec))
                self.wake_yet = True

            if elapsed_sec == (60.0 * 30):
                self.nao.sit_say('Yawn_1','I am getting sleepy')
                self.nao.log('class=SleepySubscriber|method=callback|action=tired|elapsed_sec=' + str(elapsed_sec))



    def setup(self):
        self.nao.log('class=SleepySubscriber|method=setup')
            

    def tear_down(self):
        self.nao.log('class=SleepySubscriber|method=teardown')
        