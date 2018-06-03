'''
Created on 1 April 2014
@author: Don Najd
@description: Nao will be Sociable
'''
# python
from __future__ import print_function

# SIGINT
import signal
import sys

# naoutil & fluentnao
from naoutil import broker
import naoutil.naoenv as naoenv
import naoutil.memory as memory
from fluentnao.nao import Nao
#import expressions.anim as anim

# subscribers
from subscribers.sleepy_subscriber import SleepySubscriber
from subscribers.look_around_subscriber import LookAroundSubscriber
from subscribers.greeting_subscriber import GreetingSubscriber
from subscribers.star_trek_subscriber import StarTrekSubscriber
from subscribers.voice_movement_subscriber import VoiceMovementSubscriber
#from subscribers.sensitive_subscriber import SensitiveSubscriber
from subscribers.random_response_subscriber import RandomResponseSubscriber

# providers
from providers.touch_provider import TouchProvider
from providers.time_provider import TimeProvider
from providers.face_recog_provider import FaceRecogProvider
from providers.voice_recog_provider import VoiceRecogProvider
#from providers.voice_emotion_provider import VoiceEmotionProvider


#########################
# SETUP: Broker

naoIp = "192.168.1.18"
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)

#########################
# SETUP: FluentNao

env = naoenv.make_environment(None)
log = lambda msg: print(msg) 				# lambda for loggin to the console
n = Nao(env, log)

# disable autonomous moves
n.env.add_proxy("ALAutonomousMoves")
autonomous_moves = n.env.proxies["ALAutonomousMoves"] 
autonomous_moves.setExpressiveListeningEnabled(False)


#########################
# SETUP: Nao Consious

#============
# subscribers
sleepy_subscriber = SleepySubscriber(n)
look_around_subscriber = LookAroundSubscriber(n)
greeting_subscriber = GreetingSubscriber(n)
star_trek_subscriber = StarTrekSubscriber(n)
voice_movement_subscriber = VoiceMovementSubscriber(n)

# responses
rand_laugh_subscriber = RandomResponseSubscriber(n, ['ha ha', 'l o l', 'o m g', 'wow', 'oh god'])
rand_confusion_subscriber = RandomResponseSubscriber(n, ['what is happening', 'i am confused', 'this is crazy', 'who did that'])
rand_animal_sounds_subscriber = RandomResponseSubscriber(n, ['snort', 'growl', 'screech', 'roar', 'grrrrrrr', 'buzz', 'meow', 'purr', 'hiss'])
rand_family_member_subscriber = RandomResponseSubscriber(n, ['woody', 'jovial', 'autumn', 'melissa', 'donny'], 'hey')

#============
# providers

# time provider
time_provider = TimeProvider(n)

# touch providers
ftt_touch_provider = TouchProvider(n, memory, 'FrontTactilTouched')
mtt_touch_provider = TouchProvider(n, memory, 'MiddleTactilTouched')

rbp_touch_provider = TouchProvider(n, memory, 'RightBumperPressed')
lbp_touch_provider = TouchProvider(n, memory, 'LeftBumperPressed')

#cbp_touch_provider = TouchProvider(n, memory, 'ChestButtonPressed')
#rtt_touch_provider = TouchProvider(n, memory, 'RearTactilTouched')
#hrbt_touch_provider = TouchProvider(n, memory, 'HandLeftTouched')
#hrlt_touch_provider = TouchProvider(n, memory, 'HandRightTouched')

#RightBumperPressed, LeftBumperPressed, FrontTactilTouched, MiddleTactilTouched, RearTactilTouched, HandRightBackTouched
#HandRightLeftTouched, HandRightRightTouched, HandLeftBackTouched, HandLeftLeftTouched, HandLeftRightTouched, # face recogn

face_recog_provider = FaceRecogProvider(n, memory)

# voice recogn
voice_recog_provider = VoiceRecogProvider(n, memory)

def setup():
	
	# time: sleepy & look around
	time_provider.add_subscriber(sleepy_subscriber)
	time_provider.add_subscriber(look_around_subscriber)
	time_provider.setup()

	# tactile: random laugh
	rbp_touch_provider.add_subscriber(rand_laugh_subscriber).setup()
	lbp_touch_provider.add_subscriber(rand_confusion_subscriber).setup()
	mtt_touch_provider.add_subscriber(rand_animal_sounds_subscriber).setup()
	ftt_touch_provider.add_subscriber(rand_family_member_subscriber).setup()

	# face recog
	face_recog_provider.add_subscriber(greeting_subscriber).setup()

	# voice recog
	#voice_recog_provider.add_subscriber(star_trek_subscriber)
	voice_recog_provider.add_subscriber(voice_movement_subscriber).setup()



#########################
# HELPER: tear down

def tear_down():
	n.sit_say('Rest_1', 'Deactivate')

	# teardown
	time_provider.tear_down()

	rbp_touch_provider.tear_down()
	lbp_touch_provider.tear_down()
	mtt_touch_provider.tear_down()
	ftt_touch_provider.tear_down()
	face_recog_provider.tear_down()
	voice_recog_provider.tear_down()

	memory.unsubscribeToEvent('RearTactilTouched')  

# sigint
def tear_down_signal_handler(signal, frame):
    tear_down()
    sys.exit(0)

signal.signal(signal.SIGINT, tear_down_signal_handler)
	
# tactil
def tear_down_tactil_handler(dataName, value, message):
	if value==1:
		tear_down()

memory.subscribeToEvent('RearTactilTouched', tear_down_tactil_handler)



#######################
# FluentNao: example of basic event & handlers

# tactil
# def right_bumper_handler(dataName, value, message):
# 	if value==1:
# 		n.say('that is my right foot')

# def left_bumper_handler(dataName, value, message):
# 	if value==1:
# 		n.say('that is my left foot')

# memory.subscribeToEvent('RightBumperPressed', right_bumper_handler)
# memory.subscribeToEvent('LeftBumperPressed', left_bumper_handler)



#######################
# trigger setup
setup()

