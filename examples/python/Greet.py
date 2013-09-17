import math
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime, timedelta
from naoutil import broker

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

    ##########################
    # Face Recog Event
    def faceCallback(self, dataName, value, message):

        # get name from naoqi
        name = value[1][1][1][0]
        if len(name) > 0:            
        
            # new person?
            if not name in self.logged_recog:

                # log greeting
                self.logged_recog[name] = datetime.now()
                self.nao.wait(1)

                # do greeting
                self.nao.naoscript.get(35)
                self.nao.go()
                self.nao.say('hello ' + name)
                
                # sit & relax
                self.nao.sit()
                  
            else:
                then = self.logged_recog[name]
                now = datetime.now()
                if now - then > timedelta(minutes=5):
                    self.nao.say('hello again ' + name)    
           
    ##########################
    # Touch Controls

    def startControlCallback(self, dataName, value, message):
        # bumper down & not running
        if value==1 and self.running == False:

            # set state
            self.running = True

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
nao = nao.Nao(env, None)

# Proxies: FaceTracker & Motion
nao.env.add_proxy("ALFaceTracker")   
facetracker = nao.env.proxies["ALFaceTracker"] 

#########################
# GO
######################### 
greet = Greet(nao, facetracker, memory)


