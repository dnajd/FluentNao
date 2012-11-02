from naoqi import ALProxy
from naoqi import ALModule
NaoEvent = None
class EventModule(ALModule):
    def __init__(self, globalName, eventLambda, eventName, log):
        ALModule.__init__(self, globalName)

        # ALMemory & Logging
        global memory
        memory = ALProxy("ALMemory")
        self.log = log
        
        # settings
        self.eventLambda = eventLambda
        self.eventName = eventName
        self.callbackModule = globalName
        self.callbackMethod = "onNaoEvent"

        # track press / release state
        self.buttonState = 0
        
        # subscribe
        self.subscribe()
        
    def toggleButtonState(self):
        if (self.buttonState == 0):
            self.buttonState = 1
        else:
            self.buttonState = 0

    def onNaoEvent(self, *_args):       
        if (self.buttonState == 0):
            # trigger lambda
            self.unsubscribe()
            self.eventLambda()
            self.subscribe()
            
        # toggle state
        self.toggleButtonState()
       
    def subscribe(self):
        memory.subscribeToEvent(self.eventName, self.callbackModule, self.callbackMethod)    

    def unsubscribe(self):
        memory.unsubscribeToEvent(self.eventName, self.callbackModule)