from naoqi import ALProxy
from naoqi import ALModule
class EventModule(ALModule):
    
    def __init__(self, globalName, eventLambda, eventName, log):
        ALModule.__init__(self, globalName)

        # ALMemory & Logging
        global memory
        memory = ALProxy("ALMemory")
        self.log = log
        
        # code to execute
        self.eventLambda = eventLambda

        # for Nao API
        self.eventName = eventName
        self.callbackModule = globalName
        self.callbackMethod = "onNaoEvent"
       
        # subscribe
        self.subscribe()
        
    def onNaoEvent(self, *_args):     
        
        # get args
        event,value,param = _args
        if value==1.0:
            pressed=True
        else:
            pressed=False  
        
        # trigger lambda
        if (pressed):
            self.unsubscribe()
            self.eventLambda()
            self.subscribe()
       
    def subscribe(self):
        memory.subscribeToEvent(self.eventName, self.callbackModule, self.callbackMethod)    

    def unsubscribe(self):
        memory.unsubscribeToEvent(self.eventName, self.callbackModule)