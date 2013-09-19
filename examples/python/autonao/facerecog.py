'''
Created on 17 Sept 2013

@author: don Najd
@description: Wrapper around face recognition
'''
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao

class FaceRecog(object):

    def __init__(self, nao, memory):

        self.running == False
        self.subscribers = []

        # args
        self.nao = nao 
        self.memory = memory

        # facetracker
        self.nao.env.add_proxy("ALFaceTracker")   
        self.facetracker = self.nao.env.proxies["ALFaceTracker"] 

        # wire touch controls
        self.memory.subscribeToEvent('FrontTactilTouched', self.startCallback)
        self.memory.subscribeToEvent('RearTactilTouched', self.stopCallback)

    # subscription
    def addSubscriber(self, subscriber):
        self.subscribers.append(subscriber)


    # face detected
    def faceDetectedCallback(self, dataName, value, message):

        # call subscribers
        for s in self.subscribers:
            s.faceRecogCallback(dataName, value, message)

           
    ##########################
    # Touch Controls

    def startCallback(self, dataName, value, message):
        # control down
        if value==1 and self.running == False:

            # status
            self.running = True
            nao.log('class=facerecog|controls=start|running=True')   

            # face track
            self.nao.env.motion.setStiffnesses("Head", 1.0)
            self.facetracker.startTracker()    

            # start
            self.memory.subscribeToEvent('FaceDetected', self.faceDetectedCallback)

            # call subscribers
            for s in self.subscribers:
                s.faceRecogStartCallback(dataName, value, message)

    def stopCallback(self, dataName, value, message):
        # control down
        if value==1 and self.running == True:

            # status
            self.running = False
            nao.log('class=facerecog|controls=stop|running=False')  

            # face track
            self.nao.env.motion.setStiffnesses("Head", 0)
            self.facetracker.stopTracker()    

            # stop
            self.memory.unsubscribeToEvent('FaceDetected')  

            # call subscribers
            for s in self.subscribers:
                s.faceRecogStopCallback(dataName, value, message)