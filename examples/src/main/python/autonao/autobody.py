'''
Created on 25 Sept 2013

@author: don Najd
@description: Nao will shift around a bit
'''
import sys
import time
from time import sleep
from threading import Thread
from random import randint

def automove(nao, autobody):

	try:
	    while autobody.run:
	    	# shift head
	    	offset_x = randint(-20,20)
	    	offset_y = randint(-10,10)
	        nao.head.forward(0, offset_x).center(0, offset_y)

	        # sleep
	        sleep_time = randint(0,120)
	        sleep(sleep_time)
	except KeyboardInterrupt:
	    print("Quitting the program.")
	except:
	    print("Unexpected error: "+ str(sys.exc_info()[0]))
	    raise

class Autobody(object):

	def __init__(self, nao):

		# start running
		self.run = True

		# thread to return control
		t = Thread(target=automove, args=(nao,self,))
		t.start()

	