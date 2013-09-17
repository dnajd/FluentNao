import math
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime, timedelta
from naoutil import broker

def faceCallback(dataName, value, message):
    #self.log(value)

    # get name
    name = value[1][1][1][0]
    if len(name) > 0:            
    
        # new person?
        if not name in names:

            # log greeting
            names[name] = datetime.now()
            nao.wait(1)

            # do greeting
            nao.naoscript.get(35)
            nao.go()
            nao.say('hello ' + name)
            
            # sit & relax
            nao.sit()
              
        else:
            then = names[name]
            now = datetime.now()
            if now - then > timedelta(minutes=1):
                nao.say('hello again ' + name)    
       

def startCallback(dataName, value, message):
    # bumper down
    if value==1:
        # face track
        motion.setStiffnesses("Head", 1.0)
        facetracker.startTracker()    

        # start
        nao.sit()
        nao.say('start behavior')
        memory.subscribeToEvent('FaceDetected', faceCallback)

def cancelCallback(dataName, value, message):
    # bumper down
    if value==1:

        # stop face track
        facetracker.stopTracker()    
        motion.setStiffnesses("Head", 0)

        # cancel
        nao.say('cancel behavior')
        memory.unsubscribeToEvent('FaceDetected')  
        nao.sit()
        nao.wait(3)
        nao.relax()


#########################
# MAIN SETUP
######################### 

# Broker (must come first)
broker.Broker('bootstrapBroker', naoIp="nao.local", naoPort=9559)

# FluentNao
env = naoenv.make_environment(None)
nao = nao.Nao(env, None)

# Proxies: FaceTracker & Motion
nao.env.add_proxy("ALFaceTracker")   
facetracker = nao.env.proxies["ALFaceTracker"] 
motion = nao.env.motion  

#########################
# MAIN EVENT
######################### 

# names
names = {}    

# start / cancel controls
memory.subscribeToEvent('FrontTactilTouched', startCallback)
memory.subscribeToEvent('RearTactilTouched', cancelCallback)
