-FluentNao
=================

Control Nao using fluent stanza of python code.

Example Code
======================
Here is an example to make nao fight.

    # zero out joints
    nao.zero().go()

    # set duration for movements
    nao.setDuration(.5)

    # get ready
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
You need to include the FluentNao python class files in your "Project References" Panel.  Then include the following in a script box.

Importing the API
-----------------
    # import
    try:
        from fluentnao import nao
    except:
        import sys
        sys.path.append(ALFrameManager.getBehaviorPath(self.behaviorId))
        from fluentnao import nao
        reload(nao)

    # start using
    from fluentnao.nao import Nao
    nao = Nao(ALProxy, self.log)

With this the robot will be able to find and import the python classes. 


Contributing
============
I'm developing in [Sublime Text 2](http://www.sublimetext.com/2 "Sublime Text 2"). My examples below assume you have cloned the github repository to /development/FluentNao/

Developing in Choregraphe
-----------
NOTE: This only works in Choregraphe and not on the actual robot.  To make changes to FluentNao python code in a fast and easy way, you should run your scripts on the simulated robot.  Include the following in your Choregraphe script box to develop & test quickly and easily.

    # import
    pathToCore = "/development/FluentNao/"
    try:
        from fluentnao import nao
    except:
    	import sys
    	sys.path.append(pathToCore)
	from fluentnao import nao
    reload(nao)
    nao.initModulesForDevelopment(pathToCore)

    # start using
    from fluentnao.nao import Nao
    nao = Nao(ALProxy, self.log)

This code helps python reference FluentNao modules and classes directly from the git repository you cloned. It also informs python that it should reload the modules and classes each time you run your behavior. 



