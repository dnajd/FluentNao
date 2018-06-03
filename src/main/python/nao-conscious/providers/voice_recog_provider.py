'''
Created on 5 June 2014

@author: Don Najd
@description: Provider for Naoqi Voice Recog
'''
from time import sleep

class VoiceRecogProvider(object):

    def __init__(self, nao, memory):

        # args
        self.nao = nao 
        self.memory = memory

        # provider properties
        self.running = False
        self.subscribers = []
        self.vocab = []

        # log
        self.nao.log('class=VoiceRecogProvider|method=__init__')   

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
        self.nao.log('class=VoiceRecogProvider|method=add_subscriber')  
        return self

    def setup(self):

        # append all vocabularies
        for s in self.subscribers:
            self.vocab += s.vocab

        # disable audio & visual expression
        self.nao.env.speechRecognition.setAudioExpression(False)
        self.nao.env.speechRecognition.setVisualExpression(True)

        # disable autonomous moves
        self.nao.env.add_proxy("ALAutonomousMoves")
        autonomous_moves = self.nao.env.proxies["ALAutonomousMoves"] 
        autonomous_moves.setExpressiveListeningEnabled(False)

        # init vocab
        self.nao.env.speechRecognition.setVocabulary(self.vocab, False)

        # subscribe event
        self.memory.subscribeToEvent('WordRecognized', self.event_callback)
        
        self.nao.log('class=VoiceRecogProvider|method=setup')  

    def tear_down(self):
        self.memory.unsubscribeToEvent('WordRecognized')
        self.nao.log('class=VoiceRecogProvider|method=teardown')  

    def event_callback(self, naoqi_dataName, naoqi_value, naoqi_message): 

        if self.running == False:

            # status
            self.running = True
            self.nao.log('class=VoiceRecogProvider|method=event_callback|action=call_subscribers')  

            # zip into dictionary; {phrase: confidence}
            naoqi_value = dict(zip(naoqi_value[0::2], naoqi_value[1::2]))

            # call subscribers
            for s in self.subscribers:
                s.callback(naoqi_dataName, naoqi_value, naoqi_message)

            sleep(2)
            self.nao.log('class=VoiceRecogProvider|method=event_callback|action=call_subscribers_complete')  
            self.running = False 

            