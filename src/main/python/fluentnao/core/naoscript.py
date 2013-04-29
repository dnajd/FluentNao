from joints import Joints
import httplib
import json

class NaoScript():

    # init method
    def __init__(self, nao):
        
        self.nao = nao
        self.log = nao.log

    def go(self):
        self.nao.go()
        
    ###################################
    # noascript
    ###################################
    def get(self, scriptId):  
        
        # setup
        uri = 'naoscript.herokuapp.com'
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

        # connect & request
        conn = httplib.HTTPConnection(uri)
        conn.request("GET", "/behaviors/" + str(scriptId) + ".json", "", headers)

        # response & read
        response = conn.getresponse()
        data = response.read()

        # close
        conn.close()

        # parse json
        json_result = json.loads(data)
        
        # run script
        script = str(json_result['script']).strip()
        self.run_script(script, '\r\n')

        return self;

    def run_script(self, cmds, split_str=";"):
        line = 0;
        try:
            if (len(cmds) > 0):
                for cmd in cmds.split(split_str):
                    line += 1
                    if not "#" in cmd:
                        cmd = cmd.replace("nao.", "").strip()
                        cmd = cmd.replace(";", "").strip()
                        if (len(cmd) > 0):
                            cmd = "self.nao." + cmd
                            self.log("line " + str(line) + ": " + cmd)
                            eval(cmd)   
        except:
            self.log("errors occured")
            self.nao.say("you have an error in your code on line " + str(line))
        
