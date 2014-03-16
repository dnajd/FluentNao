'''
Created on 17 Sept 2013

@author: don Najd
@description: Nao will act autonomously
'''
from __future__ import print_function

from naoutil import broker
import naoutil.naoenv as naoenv
import naoutil.memory as memory

from fluentnao.nao import Nao
from autonao.facerecog import FaceRecog
from autonao.greet import Greet
from autonao.autobody import Autobody

#########################
# SETUP
######################### 

# Broker (must come first)
naoIp = "nao.local"
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)

# FluentNao
env = naoenv.make_environment(None)
log = lambda msg: print(msg) # lambda for loggin to the console
nao = Nao(env, log)

#########################
# GO
######################### 

# create greeter
greeter = Greet(nao)

# subscribe to face recog
faceRecog = FaceRecog(nao, memory)
faceRecog.add_subscriber(greeter)

Autobody(nao)
