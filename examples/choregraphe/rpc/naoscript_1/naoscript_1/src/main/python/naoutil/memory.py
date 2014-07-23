'''
Created on April 06, 2013

@author: AxelVoitier
@license: GNU LGPL v3

Provide helper functions to easilly subscribe to ALMemory events and micro events.
'''

from naoutil import ALModule
from naoqi import ALProxy
import weakref

def singleton(cls):
    instances = weakref.WeakValueDictionary()
    def getinstance():
        try:
            return instances[cls]
        except KeyError:
            instance = cls() # Keep a strong ref until it is returned
            instances[cls] = instance
            return instance
    return getinstance

@singleton
class _SubscriberModule(ALModule):
    def __init__(self):
        ALModule.__init__(self)
        self.memory = ALProxy('ALMemory')
        self.dataNameToMicroEventCallback = {}
        self.dataNameToEventCallback = {}
        
    def subscribeToEvent(self, dataName, callback):
        self.dataNameToEventCallback[dataName] = callback
        self.memory.subscribeToEvent(dataName, self.moduleName, 'eventCB')
        
    def unsubscribeToEvent(self, dataName):
        if dataName in self.dataNameToEventCallback:
            self.memory.unsubscribeToEvent(dataName, self.moduleName)
            del self.dataNameToEventCallback[dataName]
        
    def eventCB(self, dataName, value, message):
        self.dataNameToEventCallback[dataName](dataName, value, message)
        
    def subscribeToMicroEvent(self, dataName, callback, cbMessage):
        self.dataNameToMicroEventCallback[dataName] = callback
        self.memory.subscribeToMicroEvent(dataName, self.moduleName, cbMessage, 'microEventCB')
        
    def unsubscribeToMicroEvent(self, dataName):
        if dataName in self.dataNameToMicroEventCallback:
            self.memory.unsubscribeToMicroEvent(dataName, self.moduleName)
            del self.dataNameToMicroEventCallback[dataName]
        
    def microEventCB(self, dataName, value, message):
        self.dataNameToMicroEventCallback[dataName](dataName, value, message)
        
def subscribeToEvent(dataName, callback):
    _SubscriberModule().subscribeToEvent(dataName, callback)
        
def unsubscribeToEvent(dataName):
    _SubscriberModule().unsubscribeToEvent(dataName)
        
def subscribeToMicroEvent(dataName, callback, cbMessage=''):
    _SubscriberModule().subscribeToMicroEvent(dataName, callback, cbMessage)
        
def unsubscribeToMicroEvent(dataName):
    _SubscriberModule().unsubscribeToMicroEvent(dataName)
