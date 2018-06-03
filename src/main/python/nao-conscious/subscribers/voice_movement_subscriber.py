'''
Created on 5 June 2014

@author: Don Najd
@description: Nao will respond if star trek words are recognized
'''
import random
from datetime import datetime, timedelta

class VoiceMovementSubscriber(object):

    def __init__(self, nao):

        self.nao = nao 
        self.nao.log('class=VoiceMovementSubscriber|method=__init__')
        self.vocab = ['hands open', 'hands closed', 'arms forward', 'sit down', 'relax', 'want this', 'drop it', 'hold it', 'cancel', 'reset system', 'blue', 'red']

    def test_word(self, dict, key, word):

        t = 0.35 # confidence
        if key == word and dict[key] > t:
            return True
        return False

    def callback(self, eventName, value, subscriberIdentifier):

        self.nao.log('class=VoiceMovementSubscriber|method=callback|value=' + str(value))

        # get key with most confident match
        d = value
        key = max(d, key=d.get)
        
        # test words
        if self.test_word(d, key, 'hands open'):
            self.nao.hands.open()

        elif self.test_word(d, key, 'hands closed'):
            self.nao.hands.close()

        elif self.test_word(d, key, 'arms forward'):
            self.nao.arms.forward().elbows.straight()

        elif self.test_word(d, key, 'sit down'):
            self.nao.sit()

        elif self.test_word(d, key, 'relax'):
            self.nao.relax()

        elif self.test_word(d, key, 'want this'):
            self.nao.arms.right_forward().elbows.right_straight().hands.right_open()

        elif self.test_word(d, key, 'hold it'):
            self.nao.hands.right_close()

        elif self.test_word(d, key, 'drop it'):
            self.nao.hands.open().go()

        elif self.test_word(d, key, 'cancel'):
             # leds blink red
            self.nao.leds.off()
            self.nao.wait(.1)
            self.nao.leds.eyes(0xcc0000, .3)
            self.nao.leds.chest(0xcc0000, 1)    
            self.nao.wait(.3)
            self.nao.leds.off()

        elif self.test_word(d, key, 'reset system'):
            self.nao.stiff()
            self.nao.sit()
            self.nao.leds.eyes(0x38B0DE, .3)

        elif self.test_word(d, key, 'red'):
            self.nao.leds.chest(0xcc0000, 1)    

        elif self.test_word(d, key, 'blue'):
            self.nao.leds.chest(0x38B0DE, .3)

    def setup(self):
        self.nao.log('class=VoiceMovementSubscriber|method=setup')
            

    def tear_down(self):
        self.nao.log('class=VoiceMovementSubscriber|method=teardown')

