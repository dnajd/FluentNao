Fluent-Motion-API
=================

Control Nao's movements using fluent stanza of python code. This is useful if you want to quickly get nao into a very common position.  Useful too if you want Nao to react in many different ways based on word recognition, face recognition, random behavior.

Example Code
======================
Here is an example to make nao fight.

    # zero out joints
    nao.zero()
    nao.go()

    # ready to fight
    nao.setDuration(.5)
    nao.say("ready position")
    nao.arms.back().elbows.bent().turnUp()
    nao.go()

    # right punch
    nao.setDuration(.3)
    nao.say("throw two punches")
    nao.arms.rForward().elbows.rStraight().rTurnIn()
    nao.go()
 
    # left punch
    nao.arms.rBack().lForward()
    nao.elbows.rBent().rTurnUp()
    nao.elbows.lStraight().lTurnIn()
    nao.go()
 
    # bring left back
    nao.setDuration(1)
    nao.say("ready position")
    nao.arms.lBack().elbows.lBent().lTurnUp()
    nao.go()

    # muscle man
    nao.say("Look at me")
    nao.arms.out().elbows.bent().turnUp()
    nao.go()
    nao.say("I am strong")

Duration of Movement
--------------------
You can specify a number of seconds to take for each command or stanza. We use the setDuration() to set the duration globally for every function that follows

    # sets duration to half a second 
    nao.setDuration(.5)

We can override the default duration in each motion function

    # open hands in half a second
    nao.hands.open()

    # put arms out in 4 seconds
    nao.arms.out(4)
    nao.go()

NOTE: passing in a duration of 0 will be ignored

Offsets
--------------------
You can offset any motion, adding more or less degrees of movement.  For example

    # zero out joints
    nao.zero().go()

    # put arms up minus 30 degrees
    nao.arms.up(0, -30)

NOTE: the zero is duration telling the api to ignore that argument;


In Choregraphe
=================
You need to include the Fluent-Motion-API python class files in your "Project References" Panel.  Then include the following in a script box.

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

