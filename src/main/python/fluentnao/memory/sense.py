from fluentnao.memory.eventModule import EventModule
from fluentnao.core.joints import Joints
class Sense():
    def __init__(self, nao):       
        
        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log


    def left_bumper(self, eventLambda):
        eventName = Joints().Events.Bumper.LeftBumperPressed
        
        # register event
        global LBEvent
        globalName = "LBEvent"
        LBEvent = EventModule(globalName, eventLambda, eventName, self.log)      
        self.log("subscribed " + globalName)

    def right_bumper(self, eventLambda):
        eventName = Joints().Events.Bumper.RightBumperPressed
        
        # register event
        global RBEvent
        globalName = "RBEvent"
        RBEvent = EventModule(globalName, eventLambda, eventName, self.log)      
        self.log("subscribed " + globalName)
