FluentNao
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
To use FluentNao in choregraphe, check out the example behavior ./examples/choregraphe/fluentnao.crg

This behavior includes the FluentNao modules and classes as project references.  It contains the python code needed to import and use FluentNao.


Contributing
============
I'm developing in [Sublime Text 2](http://www.sublimetext.com/2 "Sublime Text 2") and Eclipse. 

1. Clone the github repository
2. Check out ./examples/choregraphe/development/fluentnao_dev.crg

This behavior will run FluentNao modules and classes from your clone of the repository.  This behavior can run the FluentNao modules and classes against the local naoqi or the simulator.  When you update FluentNao, everything will be reloaded and changes will take effect immediately.

NOTE: you must update pathToFluentNao in the FluentNao Script Box

