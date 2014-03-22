
'''
Created on 22 March 2014

@author: don Najd
@description: Nao respond to star trek words
'''

import math
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime
from naoutil import broker

class Startrek(object):


    def __init__(self, nao):

        # args
        self.nao = nao 

        # class state
        self.logged_recog = {}  

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

		#key = 'sit'
		#if key in d and d[key] > t:
	#		self.nao.sit()

		#key = 'wake'
		#if key in d and d[key] > t:
	#		self.nao.stiff()
		
	#	key = 'sleep'
	#	if key in d and d[key] > t:
	#		self.nao.relax()

		key = 'data'
		if key in d and d[key] > t:
			self.nao.say('yes what do you want')

		key = 'phasers'
		if key in d and d[key] > t:
			self.nao.say('fire when ready')

		key = 'tractor'
		if key in d and d[key] > t:
			self.nao.say('engage and pull them in')

		key = 'hailing'
		if key in d and d[key] > t:
			self.nao.say('bring up visuals')

		key = 'torpedo'
		if key in d and d[key] > t:
			self.nao.say('shields up')

		key = 'shields'
		if key in d and d[key] > t:
			self.nao.say('holding at 20 percent')

		key = 'purple'
		if key in d and d[key] > t:
			self.nao.say('jovial loves that color')

	# speech recogn
	vocab = ['sit','wake', 'sleep', 'data', 'phasers', 'tractor', 'hailing', 'torpedo', 'shields', 'purple']
	self.nao.env.speechRecognition.setVocabulary(vocab, True)

	# on / off
	memory.subscribeToEvent('FrontTactilTouched', subscribe_callback)
	memory.subscribeToEvent('RearTactilTouched', unsubscribe_callback)
