
import math
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime
from naoutil import broker

# naoutil broker & env
naoIp = "192.168.2.13"
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)
env = naoenv.make_environment(None) #using broker don't need ->, ipaddr="nao.local", port=9559)

# FluentNao
nao = nao.Nao(env, None)


def doSomething():
	nao.arms.forward().elbows.bent()
	nao.say('I did something')


# subscribe
# callbacks
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
	print value

	# zip into dictionary
	d = dict(zip(value[0::2], value[1::2]))
	t = .58

	key = 'stand'
	if key in d and d[key] > t:
		self.nao.stand()

	key = 'sit'
	if key in d and d[key] > t:
		self.nao.sit()

	key = 'crouch'
	if key in d and d[key] > t:
		self.nao.crouch()

	key = 'arms forward'
	if key in d and d[key] > t:
		self.nao.arms.forward()

	key = 'arms out'
	if key in d and d[key] > t:
		self.nao.arms.out()

	key = 'hands open'
	if key in d and d[key] > t:
		self.nao.hands.open()

	key = 'hands closed'
	if key in d and d[key] > t:
		self.nao.hands.close()

# speech recogn
vocab = ['stand','sit', 'crouch', 'arms forward', 'arms out', 'hands open', 'hands closed']
nao.env.speechRecognition.setVocabulary(vocab, True)

# on / off
memory.subscribeToEvent('FrontTactilTouched', subscribe_callback)
memory.subscribeToEvent('RearTactilTouched', unsubscribe_callback)


# events you can use
#RightBumperPressed, LeftBumperPressed, ChestButtonPressed, FrontTactilTouched
#MiddleTactilTouched, RearTactilTouched, HotJointDetected, HandRightBackTouched, HandRightLeftTouched
#HandRightRightTouched, HandLeftBackTouched, HandLeftLeftTouched, HandLeftRightTouched
#BodyStiffnessChanged, SimpleClickOccured, DoubleClickOccured, TripleClickOccured
#WordRecognized, LastWordRecognized, SpeechDetected" https://community.aldebaran-robotics.com/doc/1-14/naoqi/audio/alspeechrecognition-api.html#ALSpeechRecognitionProxy::setVisualExpression__bCR

#broker.shutdown()
