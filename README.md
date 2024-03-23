# FluentNao

Control Nao using fluent stanza of python code.

# Requirements

All you need is docker and a nao robot connected to the same network as your computer.

# Setup

Push the button on Nao's chest to get it's IP address and set it in your terminal

```
export NAO_IP=###.###.###.###
```

# Get Started

`make`   - see all make targets

Build the docker container

`init` - build the docker image

Run the container

`up`  - run interactive shell

That loads up the interactive python prompt and you can use the commands below to control nao

    nao.say('wow this is awesome')

If you'd like to see nao be interactive and conscious run this one

    ./nao-conscious

tap the head sensor in the back to deactivate

# Example Code

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

## Duration of Movement

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

## exOffsets

You can offset any motion, adding more or less degrees of movement.  For example

    # zero out joints
    nao.zero().go()

    # put arms up minus 30 degrees
    nao.arms.up(0, -30)

NOTE: the zero is duration telling the api to ignore that argument;

