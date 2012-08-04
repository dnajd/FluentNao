Fluent-Motion-API
=================

Control Nao's movements using python code; Here is what the code would look like in a Choregraphe script box:

	def onInput_onStart(self):

    	# Create Motion Class
    	motionProxy = ALProxy("ALMotion")
    	nao = FluentMotion(motionProxy, self.log)

     	# zero out joints
     	nao.zero().go()

     	# animates arms up and hands forward
     	nao.armsUp().handsForward().go()
 
	pass

This is useful if you want to quickly get nao into a very common position.  Ex. Hands over head, stand on one foot, hang head, etc.  Useful too if you want Nao to react in many different ways based on word recognition, face recognition, random behavior.


Setting Up
=================

Development
-----------
I'm developing in [Sublime Text 2](http://www.sublimetext.com/2 "Sublime Text 2"); I recomend installing and editing python code using this IDE

GitHub
-----------
My examples below assume you have cloned the repo to ~/development/Fluent-Motion-API

Choregraphe
-----------
To make development fast and easy, include this in your Choregraphe script box

	try:
    	import fluentMotion
    except:
    	import sys
        sys.path.append("~/development/Fluent-Motion-API/core")
        import fluentMotion

        reload(fluentMotion)

This code helps python reference the Fluent-Motion-API classes and reloads them every time so changes will go into affect as you develop

On The Robot
------------
To push the behavior to the robot you must include the Fluent-Motion-API python class files in your Project References Panel, in Choregraphe.  Then in your script box update the import code above to the following.

	try:
    	import fluentMotion
    except:
    	import sys
        sys.path.append(ALFrameManager.getBehaviorPath(self.behaviorId))
        import fluentMotion

        reload(fluentMotion)

With this the robot will be able to find and import the python classes.  Here is a simple example that zeros out all nao's joints and then make him raise his arms up:

    # Create Motion Class
    motionProxy = ALProxy("ALMotion")
    nao = FluentMotion(motionProxy, self.log)

    # zero out joints & put arms up
    nao.zero().go()
    nao.armsUp().go()
