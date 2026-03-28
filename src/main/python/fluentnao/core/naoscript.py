"""Fetch and execute scripts from the naoscript.herokuapp.com service.

Accessed via nao.naoscript. Python 2.7 compatible.
"""
import httplib
import json

class NaoScript():
    """Fetches and executes scripts from the naoscript.herokuapp.com service.

    Scripts are fetched by numeric ID, parsed as JSON, and executed line
    by line using eval(). Commands are prefixed with 'self.nao.' before
    evaluation. Lines containing '#' are treated as comments and skipped.

    Warning:
        run_script() uses eval() to execute arbitrary code strings and
        swallows all exceptions. Prefer the FluentNao HTTP bridge for
        new development.
    """

    # init method
    def __init__(self, nao):
        
        self.nao = nao
        self.log = nao.log

    def go(self):
        """Wait for queued movements to complete. Returns the nao instance."""
        self.nao.go()
        return self.nao

    ###################################
    # noascript
    ###################################
    def get(self, scriptId):
        """Fetch a script by ID from naoscript.herokuapp.com and execute it."""

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
        """Parse and execute a delimited string of nao commands via eval().

        Args:
            cmds: String of commands (e.g. 'say("hi"); hands.open()').
            split_str: Delimiter between commands (default ';').
        """
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
        
