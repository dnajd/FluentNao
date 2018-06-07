FluentNao
=================

Control Nao using fluent stanza of python code.

SETUP
==========================

Edit the `bootstrap.py` and set your nao's ipaddress on line 10 (remember to use YOUR nao's ipaddress)

    naoIp = "192.168.1.18"

Edit src/main/python/fluentnao/nao.py

Docker
==========================
Times have changed and naoqi has not been kept up-to-date.  So we'll begin by building a docker image

    docker-compose build fluentnao

Starting up an interactive shell

    docker-compose run fluentnao bash

Running the old reliable bootstrap shell script

    ./bootstrap

That loads up the interactive python prompt and you can use the commands below to control nao

    nao.say('wow this is awesome')

If you'd like to see nao be interactive and conscious run this one

    ./nao-conscious

tap the head sensor in the back to deactivate

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

