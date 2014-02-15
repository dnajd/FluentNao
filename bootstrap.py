
import math
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime
from naoutil import broker

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

# broker (must come first)
naoIp = "192.168.2.13"
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)

# nao env
env = naoenv.make_environment(None) #using broker don't need ->, ipaddr="nao.local", port=9559)

# fluent nao
nao = nao.Nao(env, None)

# events
def unsubscribe_callback(dataName, value, message):
	memory.unsubscribeToEvent('FrontTactilTouched')
	memory.unsubscribeToEvent('WordRecognized')


def subscribe_callback(dataName, value, message):
	memory.subscribeToEvent('FrontTactilTouched', tactil_callback)
	memory.subscribeToEvent('WordRecognized', speech_callback)


def tactil_callback(dataName, value, message):

	if value==1:
		print 'pressed'
	else:
		print 'released'

def speech_callback(dataName, value, message):

	# zip into dictionary
	d = dict(zip(value[0::2], value[1::2]))

	if d['yes'] > 0.5:
		print d['yes']

# set vocab
vocab = ['yes','no']
nao.env.speechRecognition.setVocabulary(vocab, True)

memory.subscribeToEvent('FrontTactilTouched', subscribe_callback)
memory.subscribeToEvent('RearTactilTouched', unsubscribe_callback)

# subscribe

# events you can use
#RightBumperPressed, LeftBumperPressed, ChestButtonPressed, FrontTactilTouched
#MiddleTactilTouched, RearTactilTouched, HotJointDetected, HandRightBackTouched, HandRightLeftTouched
#HandRightRightTouched, HandLeftBackTouched, HandLeftLeftTouched, HandLeftRightTouched
#BodyStiffnessChanged, SimpleClickOccured, DoubleClickOccured, TripleClickOccured
#WordRecognized, LastWordRecognized, SpeechDetected" https://community.aldebaran-robotics.com/doc/1-14/naoqi/audio/alspeechrecognition-api.html#ALSpeechRecognitionProxy::setVisualExpression__bCR

#broker.shutdown()
