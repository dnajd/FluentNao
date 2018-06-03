FluentNao
=================

Control Nao using fluent stanza of python code.

Docker
==========================
Times have changed and naoqi has not been kept up-to-date.  So we'll begin by building a docker image

    docker-compose build fluentnao

Starting up an interactive shell

    docker-compose run fluentnao bash

Edit the `bootstrap.py` and set your nao's ipaddress on line 10 (remember to use YOUR nao's ipaddress)

    naoIp = "192.168.1.18"

Running the old reliable bootstrap shell script

    ./bootstrap

That loads up the interactive python prompt and you can use the commands below to control nao

    nao.say('wow this is awesome')


Example Code
======================

Example code using Fluent Nao

    # zero out joints
    nao.zero().go()

    # arms up
    nao.say("raising my hands") 
    nao.arms.up()
    nao.go() 
 
    # hands open
    nao.say("opening my hands") 
    nao.hands.open()
    nao.go() 

Duration of Movement
--------------------
You can specify a number of seconds to take for each command or stanza. We use the setDuration() to set the duration globally for every function that follows

    # sets duration to half a second 
    nao.set_duration(.5)

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

