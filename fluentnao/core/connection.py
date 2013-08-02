from joints import Joints
import httplib
import json

class Connection():

    # init method
    def __init__(self, nao):
        
        self.nao = nao
        self.log = nao.log

    def go(self):
        self.nao.go()
        
    ###################################
    # noascript
    ###################################
    def get(self, id):  
	
	# setup
	uri = 'naoscript.herokuapp.com'
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

	# connect & request
	conn = httplib.HTTPConnection(uri)
	conn.request("GET", "/behaviors/" + str(id) + ".json", "", headers)

	# response & read
	response = conn.getresponse()
	data = response.read()

	# close
	conn.close()

	# parse json
	json_result = json.loads(data)
	
	# run script
	script = str(json_result['script'])
	self.run_script(script)

        return self;

    def run_script(self, cmds):
        line = 0;
        try:
            if (len(cmds) > 0):
                for cmd in cmds.split(";"):
                    line += 1
                    if not "#" in cmd:
                        self.log(cmd)
                        cmd = cmd.strip().replace("nao.", "").strip()
                        if (len(cmd) > 0):
                            eval("self.nao." + cmd)   
        except:
            self.log("errors occured")
            self.nao.say("you have an error in your code on line " + str(line))
        
