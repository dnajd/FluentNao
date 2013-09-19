'''
Created on 17 Sept 2013

@author: don Najd
@description: Nao will greet autonomously
'''
from autonao.person import Person
from datetime import datetime, timedelta
import random

class Greet(object):

    def __init__(self, nao):

        self.greetings = ['Greetings', 'Hello','Hello there','Hey','Hi','Hi there','How are you','How are you doing','Howdy','Hows it going','Salutations','Sup','Whats up','Yo']

        # args
        self.nao = nao 

        # class state
        self.logged_recog = {}  


    # GREETINGS
    def rand_greeting(self):
        
        i = random.randint(0,len(self.greetings))
        return self.greetings[i]

    def play_greeting(self, person):

        # log greeting
        person.track_recognition()
        self.nao.wait(1)

        # do greeting
        self.nao.naoscript.get(35)
        self.nao.go()
        self.nao.say(self.rand_greeting() + ' ' + person.name)
        
        # sit & relax
        self.nao.sit()


    # CALLBACKS
    def callback(self, dataName, value, message):

        # get name from naoqi
        #nao.log(''.join(str(e) for e in value))
        try:
            name = value[1][1][1][0]
        except IndexError:
            name = ''

        if len(name) > 0:    

            self.nao.log('class=Greet|method=callback|name=' + str(name))
        
            # new person?
            if not name in self.logged_recog:

                # create & log person
                person = Person(name)
                self.logged_recog[name] = person

                # greet
                self.play_greeting(person)
            else:

                 # greet?
                person = self.logged_recog[name]
                if person.recog_more_than_mins(5):
                    self.play_greeting(person)


    def setup(self):

            self.nao.sit()

    def teardown(self):

            self.nao.sit()
            self.nao.wait(3)
            self.nao.relax()