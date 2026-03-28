"""
NaoScript module for fetching and executing scripts from the naoscript.herokuapp.com service.

Python 2.7 compatible. Accessed via nao.naoscript (instance of NaoScript class).

Methods
-------
  - get(scriptId)
      Fetches a script by numeric ID from naoscript.herokuapp.com/behaviors/<id>.json,
      parses the JSON response, and executes the 'script' field. Lines are split on
      '\\r\\n'. Returns self.

  - run_script(cmds, split_str=';')
      Parses a string of semicolon-delimited (or custom delimiter) commands and
      executes each one. Each command has 'nao.' stripped and is prefixed with
      'self.nao.' before being passed to eval(). Lines containing '#' are skipped
      (treated as comments). Returns nothing.

  - go()
      Calls nao.go() to wait for any queued movements to complete. Returns the
      nao instance (not self).

WARNING: run_script() uses eval() to execute arbitrary code strings and swallows
all exceptions with a generic error message. This is a security and debugging
concern. Prefer sending commands directly via the FluentNao HTTP bridge instead
of using this module for new development.

Usage Examples
--------------
    # Fetch and run a script from the naoscript service
    nao.naoscript.get(42)

    # Run a semicolon-delimited script string directly
    nao.naoscript.run_script('say("hello"); hands.open(); go()')

    # Wait for queued movements
    nao.naoscript.go()
"""
import httplib
import json

class NaoScript():

    # init method
    def __init__(self, nao):
        
        self.nao = nao
        self.log = nao.log

    def go(self):
        self.nao.go()
        return self.nao

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
        except Exception:
            self.log("errors occurred")
            self.nao.say("you have an error in your code on line " + str(line))
        
