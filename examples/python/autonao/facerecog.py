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
        self.memory.subscribeToEvent('FrontTactilTouched', self.start_callback)
        self.memory.subscribeToEvent('RearTactilTouched', self.stop_callback)


    # SUBSCRIPTION
    def add_subscriber(self, subscriber):

        self.subscribers.append(subscriber)


    # FACE DETECTED
    def face_detected_callback(self, dataName, value, message):

        # call subscribers
        for s in self.subscribers:
            s.callback(dataName, value, message)


    # TOUCH CONTROLS
    def start_callback(self, dataName, value, message):

        # control down
        if value==1 and self.running == False:

            # status
            self.running = True
            nao.log('class=facerecog|method=start_callback|controls=start|running=True')   

            # face track
            self.nao.env.motion.setStiffnesses("Head", 1.0)
            self.facetracker.startTracker()    

            # start
            self.memory.subscribeToEvent('FaceDetected', self.face_detected_callback)

            # call subscribers
            for s in self.subscribers:
                s.setup()

    def stop_callback(self, dataName, value, message):

        # control down
        if value==1 and self.running == True:

            # status
            self.running = False
            nao.log('class=facerecog|method=stop_callback|controls=stop|running=False')  

            # face track
            self.nao.env.motion.setStiffnesses("Head", 0)
            self.facetracker.stopTracker()    

            # stop
            self.memory.unsubscribeToEvent('FaceDetected')  

            # call subscribers
            for s in self.subscribers:
                s.teardown()