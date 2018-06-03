'''
Created on 17 May 2014

@author: Don Najd
@description: Nao will look around at random
'''
import random

class LookAroundSubscriber(object):

    def __init__(self, nao):

        self.nao = nao 
        self.nao.log('class=LookAroundSubscriber|method=__init__')   


    def callback(self, eventName, value, subscriberIdentifier):

        # happens every second
        #self.nao.log('class=LookAroundSubscriber|method=callback')

        if eventName == 'time_tracker':

            # time elapsed in sec
            elapsed_sec = round(float(value['elapsed_sec']))

            # chance
            chance = random.randint(1,20)
            if random.randint(1,chance) == 1:

                # offset and duration
                horz_offset = random.randint(-18,18)
                vert_offset = random.randint(-10,10)
                duration = random.uniform(.5, 2)

                # move head
                self.nao.head.forward(duration,horz_offset)
                self.nao.head.center(duration,vert_offset)

                # log
                self.nao.log('class=LookAroundSubscriber|method=callback|horz_offset={0}|vert_offset={1}|duration={2}'.format(horz_offset, vert_offset, duration))


    def setup(self):
        self.nao.log('class=LookAroundSubscriber|method=setup')
            

    def tear_down(self):
        self.nao.log('class=LookAroundSubscriber|method=teardown')
        