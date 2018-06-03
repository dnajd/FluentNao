'''
Created on April 06, 2013

@author: AxelVoitier
@license: GNU LGPL v3

Provide helper functions to easilly subscribe to ALMemory
events and micro events.
'''

from naoqi import ALProxy

from naoutil.module import Module
from naoutil.general import singleton


@singleton
class _SubscriberModule(Module):
    '''
    Singleton ALModule used to subscribe to events and micro-events.
    Not made to be used by a user.
    Prefer to call the module functions.
    '''
    def __init__(self):
        Module.__init__(self)
        self.memory = ALProxy('ALMemory')
        self.data_name_to_micro_event_cb = {}
        self.data_name_to_event_cb = {}

    # Event
    def subscribe_to_event(self, data_name, callback):
        '''
        Relay the subscription to ALMemory.
        Keep trace of the (data_name, callback) association.
        '''
        self.data_name_to_event_cb[data_name] = callback
        self.memory.subscribeToEvent(data_name, self.module_name, 'event_cb')

    def unsubscribe_to_event(self, data_name):
        '''
        Relay the unsubscription to ALMemory.
        Remove reference to the (data_name, callback) association.
        '''
        if data_name in self.data_name_to_event_cb:
            self.memory.unsubscribeToEvent(data_name, self.module_name)
            del self.data_name_to_event_cb[data_name]

    def event_cb(self, data_name, value, message):
        '''
        Callback called by ALMemory when a value change on one of the
        subscribed data_name.
        Relay to user callback.
        '''
        self.data_name_to_event_cb[data_name](data_name, value, message)

    # Micro-event
    def subscribe_to_micro_event(self, data_name, callback, cb_message):
        '''
        Relay the subscription to ALMemory.
        Keep trace of the (data_name, callback) association.
        '''
        self.data_name_to_micro_event_cb[data_name] = callback
        self.memory.subscribeToMicroEvent(data_name, self.module_name,
                                             cb_message, 'micro_event_cb')

    def unsubscribe_to_micro_event(self, data_name):
        '''
        Relay the unsubscription to ALMemory.
        Remove reference to the (data_name, callback) association.
        '''
        if data_name in self.data_name_to_micro_event_cb:
            self.memory.unsubscribeToMicroEvent(data_name, self.module_name)
            del self.data_name_to_micro_event_cb[data_name]

    def micro_event_cb(self, data_name, value, message):
        '''
        Callback called by ALMemory when a value change on one of the
        subscribed data_name.
        Relay to user callback.
        '''
        self.data_name_to_micro_event_cb[data_name](data_name, value, message)

def subscribe_to_event(data_name, callback):
    '''
    Subscribe to an event.
    '''
    _SubscriberModule().subscribe_to_event(data_name, callback)
subscribeToEvent = subscribe_to_event

def unsubscribe_to_event(data_name):
    '''
    Unsubscribe to an event.
    '''
    _SubscriberModule().unsubscribe_to_event(data_name)
unsubscribeToEvent = unsubscribe_to_event

def subscribe_to_micro_event(data_name, callback, cb_message=''):
    '''
    Subscribe to a micro-event.
    '''
    _SubscriberModule().subscribe_to_micro_event(data_name, callback,
                                                 cb_message)
subscribeToMicroEvent = subscribe_to_micro_event

def unsubscribe_to_micro_event(data_name):
    '''
    Unsubscribe to an event.
    '''
    _SubscriberModule().unsubscribe_to_micro_event(data_name)
unsubscribeToMicroEvent = unsubscribe_to_micro_event
