
import math
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime
from naoutil import broker

# broker (must come first)
broker.Broker('bootstrapBroker', naoIp="nao.local", naoPort=9559)

# nao env
env = naoenv.make_environment(None) #using broker don't need ->, ipaddr="nao.local", port=9559)

# fluent nao
nao = nao.Nao(env, None)

# create events with callbacks
#event = 'HandRightBackTouched'
#def callbackUnsubscribe(dataName, value, message):
#	memory.subscribeToEvent(event, callback)

#def callback(dataName, value, message):
#	if value==1:
#		nao.arms.stiff()
#		nao.leds.eyes(0xcc0000)
#	else:
#		nao.arms.relax()
# 		nao.leds.eyes(0x0000FF)
#memory.subscribeToEvent(event, callback)

# events you can use
#RightBumperPressed, LeftBumperPressed, ChestButtonPressed, FrontTactilTouched
#MiddleTactilTouched, RearTactilTouched, HotJointDetected, HandRightBackTouched, HandRightLeftTouched
#HandRightRightTouched, HandLeftBackTouched, HandLeftLeftTouched, HandLeftRightTouched
#BodyStiffnessChanged, SimpleClickOccured, DoubleClickOccured, TripleClickOccured