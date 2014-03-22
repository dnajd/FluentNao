
import math
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime
from naoutil import broker

# naoutil broker & env
naoIp = "192.168.2.9"
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)
env = naoenv.make_environment(None) #using broker don't need ->, ipaddr="nao.local", port=9559)

# FluentNao
nao = nao.Nao(env, None)

# subscribe

# events you can use
#RightBumperPressed, LeftBumperPressed, ChestButtonPressed, FrontTactilTouched
#MiddleTactilTouched, RearTactilTouched, HotJointDetected, HandRightBackTouched, HandRightLeftTouched
#HandRightRightTouched, HandLeftBackTouched, HandLeftLeftTouched, HandLeftRightTouched
#BodyStiffnessChanged, SimpleClickOccured, DoubleClickOccured, TripleClickOccured
#WordRecognized, LastWordRecognized, SpeechDetected" https://community.aldebaran-robotics.com/doc/1-14/naoqi/audio/alspeechrecognition-api.html#ALSpeechRecognitionProxy::setVisualExpression__bCR

#broker.shutdown()
