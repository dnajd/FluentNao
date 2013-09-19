'''
Created on 17 Sept 2013

@author: don Najd
@description: Nao will act autonomously
'''
from __future__ import print_function
import math
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime, timedelta
from naoutil import broker
import random

class Greet(object):

    def __init__(self, nao, facetracker, memory):

        # args
        self.nao = nao 
        self.facetracker = facetracker
        self.memory = memory

        # class state
        self.logged_recog = {}   
        self.running = False

        # touch controls
        self.memory.subscribeToEvent('FrontTactilTouched', self.startControlCallback)
        self.memory.subscribeToEvent('RearTactilTouched', self.cancelControlCallback)

    def get_greeting(self):
        # greetings
        greetings = ['Greetings', 'Hello','Hello there','Hey','Hi','Hi there','How are you','How are you doing','Howdy','Hows it going','Salutations','Sup','Whats up','Yo']

        # get rand greeting
        i = random.randint(0,len(greetings))
        return greetings[i]

    def do_greeting(self):

        # log greeting
        self.logged_recog[name] = datetime.now()
        self.nao.wait(1)

        # do greeting
        self.nao.naoscript.get(35)
        self.nao.go()
        self.nao.say(self.get_greeting() + ' ' + name)
        
        # sit & relax
        self.nao.sit()

    ##########################
    # Face Recog Event
    def faceCallback(self, dataName, value, message):

        #nao.log(''.join(str(e) for e in value))

        # get name from naoqi
        try:
            name = value[1][1][1][0]
        except IndexError:
            name = ''

        if len(name) > 0:    
            # log
            nao.log('face recog|name=' + str(name))
        
            # new person?
            if not name in self.logged_recog:
                self.do_greeting() # greet
            else:

                # how long ago?
                last_recog = self.logged_recog[name]
                time_past = datetime.now() - last_recog
                if time_past > timedelta(minutes=5):
                    self.do_greeting() # greet
           
    ##########################
    # Touch Controls

    def startControlCallback(self, dataName, value, message):
        # bumper down & not running
        if value==1 and self.running == False:

            # set state
            self.running = True
            nao.log('controls=start|running=True')   

            # face track
            self.nao.env.motion.setStiffnesses("Head", 1.0)
            self.facetracker.startTracker()    

            # start
            self.nao.sit()
            self.nao.say('start behavior')
            self.memory.subscribeToEvent('FaceDetected', self.faceCallback)

    def cancelControlCallback(self, dataName, value, message):
        # bumper down & running
        if value==1 and self.running == True:

            # set state
            self.running = False
            nao.log('controls=cancel|running=false')   

            # stop face track
            self.facetracker.stopTracker()    
            self.nao.env.motion.setStiffnesses("Head", 0)

            # cancel
            self.nao.say('cancel behavior')
            self.memory.unsubscribeToEvent('FaceDetected')  
            self.nao.sit()
            self.nao.wait(3)
            self.nao.relax()


#########################
# SETUP
######################### 

# Broker (must come first)
broker.Broker('bootstrapBroker', naoIp="nao.local", naoPort=9559)

# FluentNao
env = naoenv.make_environment(None)
log = lambda msg: print(msg) # lambda for loggin to the console
nao = nao.Nao(env, log)

#########################
# GO
######################### 
greet = Greet(nao, facetracker, memory)


