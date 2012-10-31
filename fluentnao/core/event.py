class Event():

    # init method
    def __init__(self, theLambda, log):
        self.theLambda = theLambda
        self.log = log
        log("test2")

    def doEvent(self, *_args):
        self.theLambda()