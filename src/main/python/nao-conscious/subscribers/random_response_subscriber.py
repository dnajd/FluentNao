'''
Created on 22 Dec 2016

@author: Don Najd
@description: Nao will simply laugh
'''

import random

class RandomResponseSubscriber(object):

    def __init__(self, nao, responses, prefix='', postfix=''):

        self.nao = nao 
        self.nao.log('class=LaughSubscriber|method=__init__')  
        
        # responses
        self.responses = responses
        self.prefix = prefix
        self.postfix = postfix

    def callback(self, eventName, value, subscriberIdentifier):

        self.nao.log('class=LaughSubscriber|method=callback')

        # laugh
        statement = self.rand_response()
        if len(self.prefix) > 0:
            self.nao.say_and_block(self.prefix)

        self.nao.say_and_block(statement)
        self.nao.wait(1)

        if len(self.postfix) > 0:
            self.nao.say(self.postfix)
            self.nao.wait(.5)

    def setup(self):
        self.nao.log('class=LaughSubscriber|method=setup')
            

    def tear_down(self):
        self.nao.log('class=LaughSubscriber|method=teardown')
        
    # greeting
    def rand_response(self):
        
        i = random.randint(0,len(self.responses))
        return self.responses[i]