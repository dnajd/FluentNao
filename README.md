Fluent-Motion-API
=================

Control Nao's movements using fluent stanza of python code; Here is what the code would look like in a Choregraphe script box:

    def onInput_onStart(self):

    	# Create Motion Class
    	motionProxy = ALProxy("ALMotion")
    	nao = FluentMotion(motionProxy, self.log)

    	# zero out joints
    	nao.zero()
	nao.go()

    	# animates arms up and hands open
    	nao.arms.up()
	nao.hands.open()
	nao.go()
 
    pass

This is useful if you want to quickly get nao into a very common position.  Useful too if you want Nao to react in many different ways based on word recognition, face recognition, random behavior.

Using The API
=================
In Choregraphe you need to include the Fluent-Motion-API python class files in your "Project References" Panel.  Then include the following in a script box.

Importing the API
-----------------
    try:
    	import fluentMotion
    	from fluentMotion import FluentMotion
    except:
    	import sys
    	sys.path.append(ALFrameManager.getBehaviorPath(self.behaviorId))
    	import fluentMotion
    	from fluentMotion import FluentMotion

With this the robot will be able to find and import the python classes. 

Scripting with the API
----------------------
Here is a example where nao fight.

    # ALTextToSpeech
    speechProxy = ALProxy("ALTextToSpeech")

    # Create Motion Class
    motionProxy = ALProxy("ALMotion")
    nao = FluentMotion(motionProxy, self.log)

    # zero out joints
    nao.zero()
    nao.go()

    # ready to fight
    nao.setDuration(.5)
    speechProxy.post.say("ready position")
    nao.arms.back().elbows.bent().turnUp()
    nao.go()

    # right punch
    nao.setDuration(.3)
    speechProxy.post.say("throw two punches")
    nao.arms.rForward().elbows.rStraight().rTurnIn()
    nao.go()
 
    # left punch
    nao.arms.rBack().lForward()
    nao.elbows.rBent().rTurnUp()
    nao.elbows.lStraight().lTurnIn()
    nao.go()
 
    # bring left back
    nao.setDuration(1)
    speechProxy.post.say("ready position")
    nao.arms.lBack().elbows.lBent().lTurnUp()
    nao.go()

    # muscle man
    speechProxy.post.say("Look at me")
    nao.arms.out().elbows.bent().turnUp()
    nao.go()
    speechProxy.post.say("I am strong")

Duration of Movement
--------------------
You can now specify a number of seconds to take for each command or stanza

Here we set the duration for each command
    # open hands in 2 seconds
    nao.hands.open(2)

    # put arms out in 4 seconds
    nao.arms.out(4)

We can use the setDuration() to set the duration globally for every command that follows

Contributing
============
I'm developing in [Sublime Text 2](http://www.sublimetext.com/2 "Sublime Text 2"). My examples below assume you have cloned the repo to /development/Fluent-Motion-API/

Choregraphe
-----------
To make changes to the Fluent-Motion-API fast and easy you should run your scripts on the simulated robot.  Include the following in your Choregraphe script box

    pathToCore = "/development/Fluent-Motion-API/core/"
    try:
    	import fluentMotion
    	from fluentMotion import FluentMotion
    except:
    	import sys
    	sys.path.append(pathToCore)
    	import fluentMotion
    	from fluentMotion import FluentMotion
            
    reload(fluentMotion)
    FluentMotion.initModulesForDevelopment(pathToCore)

This code helps python reference the Fluent-Motion-API classes directly from the git repo you cloned. It also informs python that it should reload the Fluent-Motion-API python classes each time you run your behavior. This wont work on the actual robot.

