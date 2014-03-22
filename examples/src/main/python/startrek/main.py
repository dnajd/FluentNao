'''
Created on 22 Mar 2013

@author: don Najd
@description: Nao will act autonomously
'''
from __future__ import print_function

from naoutil import broker
import naoutil.naoenv as naoenv
import naoutil.memory as memory

from fluentnao.nao import Nao
from startrek import Startrek

#########################
# SETUP
######################### 

# Broker (must come first)
naoIp = "192.168.2.10"
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)

# FluentNao
env = naoenv.make_environment(None)
log = lambda msg: print(msg) # lambda for loggin to the console
nao = Nao(env, log)

#########################
# GO
######################### 

# create greeter
startrek = Startrek(nao)

nao.say('touch my front head sensor to start')
nao.wait(2)
nao.say('rear head sensor to stop')
