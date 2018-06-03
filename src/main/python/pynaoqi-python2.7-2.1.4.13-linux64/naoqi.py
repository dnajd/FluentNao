import os
import sys
import ctypes
import weakref
import logging
import inspect
import qi

def load_inaoqi_deps():
    """ Helper to laod _inaoqi.so deps on linux """
    deps = [
            "libboost_python.so",
            "libboost_system.so",
            "libboost_chrono.so",
            "libboost_program_options.so",
            "libboost_thread.so",
            "libboost_filesystem.so",
            "libboost_regex.so",
            "libboost_locale.so",
            "libboost_signals.so",
            "libqi.so",
            "libqitype.so",
            "libalerror.so",
            "libalthread.so",
            "libalvalue.so",
            "libqimessaging.so",
            "libalcommon.so",
            "libalproxies.so",
            "libalpythontools.so",
            "libalbehavior.so",
            "libqipython.so",

    ]
    this_dir = os.path.abspath(os.path.dirname(__file__))
    for dep in deps:
        full_path = os.path.join(this_dir, dep)
        try:
            ctypes.cdll.LoadLibrary(full_path)
        except Exception:
            pass

if sys.platform.startswith("linux"):
    load_inaoqi_deps()

import inaoqi

import motion
import allog

def _getMethodParamCount(func):
    r = inspect.getargspec(func)
    #normal args
    np = len(r[0])
    #*args (none if non existent)
    if r[1] is not None:
        np = np + 1
    #**kargs  (none if non existent)
    if r[2] is not None:
        np = np + 1
    return np

def autoBind(myClass, bindIfnoDocumented):
  """Show documentation for each
  method of the class"""

  # dir(myClass) is a list of the names of
  # everything in class
  myClass.setModuleDescription(myClass.__doc__)

  for thing in dir(myClass):
    # getattr(x, "y") is exactly: x.y
    function = getattr(myClass, thing)
    if callable(function):
        if (type(function) == type(myClass.__init__)):
            if (bindIfnoDocumented or function.__doc__ != ""):
                if (thing[0] != "_"):  # private method
                    if (function.__doc__):
                        myClass.functionName(thing, myClass.getName(), function.__doc__)
                    else:
                        myClass.functionName(thing, myClass.getName(), "")

                    for param in function.func_code.co_varnames:
                        if (param != "self"):
                            myClass.addParam(param)
                        myClass._bindWithParam(myClass.getName(),thing, _getMethodParamCount(function)-1)



class ALDocable():
  def __init__(self, bindIfnoDocumented):
    autoBind(self,bindIfnoDocumented)


# define the log handler to be used by the logging module
class ALLogHandler(logging.Handler):
  def __init__(self):
    logging.Handler.__init__(self)

  def emit(self, record):
    level_to_function = {
      logging.DEBUG: allog.debug,
      logging.INFO: allog.info,
      logging.WARNING: allog.warning,
      logging.ERROR: allog.error,
      logging.CRITICAL: allog.fatal,
    }
    function = level_to_function.get(record.levelno, allog.debug)
    function(record.getMessage(),
             record.name,
             record.filename,
             record.funcName,
             record.lineno)


# Same as above, but we force the category to be behavior.box
# *AND* we prefix the message with the module name
# look at errorInBox in choregraphe for explanation
class ALBehaviorLogHandler(logging.Handler):
  def __init__(self):
    logging.Handler.__init__(self)

  def emit(self, record):
    level_to_function = {
      logging.DEBUG: allog.debug,
      logging.INFO: allog.info,
      logging.WARNING: allog.warning,
      logging.ERROR: allog.error,
      logging.CRITICAL: allog.fatal,
    }
    function = level_to_function.get(record.levelno, allog.debug)
    function(record.name + ": " + record.getMessage(),
             "behavior.box",
             "",   # record.filename in this case is simply '<string>'
             record.funcName,
             record.lineno)

# define a class that will be inherited by both ALModule and ALBehavior, to store instances of modules, so a bound method can be called on them.
class NaoQiModule():
  _modules = dict()

  @classmethod
  def getModule(cls, name):
    # returns a reference a module, giving its string, if it exists !
    if(name not in cls._modules):
      raise RuntimeError("Module " + str(name) + " does not exist")
    return cls._modules[name]()

  def __init__(self, name, logger=True):
    # keep a weak reference to ourself, so a proxy can be called on this module easily
    self._modules[name] = weakref.ref(self)
    self.loghandler = None
    if logger:
        self.logger = logging.getLogger(name)
        self.loghandler = ALLogHandler()
        self.logger.addHandler(self.loghandler)
        self.logger.setLevel(logging.DEBUG)

  def __del__(self):
    # when object is deleted, clean up dictionnary so we do not keep a weak reference to it
    del self._modules[self.getName()]
    if(self.loghandler != None):
        self.logger.removeHandler(self.loghandler)


class ALBroker(inaoqi.broker):
    def init(self):
        pass

class ALModule(inaoqi.module, ALDocable, NaoQiModule):

  def __init__(self,param):
    inaoqi.module.__init__(self, param)
    ALDocable.__init__(self, False)
    NaoQiModule.__init__(self, param)
    self.registerToBroker()

  def __del__(self):
    NaoQiModule.__del__(self)

  def methodtest(self):
    pass

  def pythonChanged(self, param1, param2, param3):
    pass


class ALBehavior(inaoqi.behavior, NaoQiModule):
  # class var in order not to build it each time
  _noNeedToBind = set(dir(inaoqi.behavior))
  _noNeedToBind.add("getModule")
  _noNeedToBind.add("onLoad")
  _noNeedToBind.add("onUnload")
  # deprecated since 1.14 methods
  _noNeedToBind.add("log")
  _noNeedToBind.add("playTimeline")
  _noNeedToBind.add("stopTimeline")
  _noNeedToBind.add("exitBehavior")
  _noNeedToBind.add("gotoAndStop")
  _noNeedToBind.add("gotoAndPlay")
  _noNeedToBind.add("playTimelineParent")
  _noNeedToBind.add("stopTimelineParent")
  _noNeedToBind.add("exitBehaviorParent")
  _noNeedToBind.add("gotoAndPlayParent")
  _noNeedToBind.add("gotoAndStopParent")

  # but we want to bind setParameter to listen runtime changes
  _noNeedToBind.remove("setParameter")

  def __init__(self, param, autoBind, brokerRegister=True):
    inaoqi.behavior.__init__(self, param)
    NaoQiModule.__init__(self, param, logger=False)
    self.logger = logging.getLogger(param)
    self.behaviorloghandler = ALBehaviorLogHandler()
    self.logger.addHandler(self.behaviorloghandler)
    self.logger.setLevel(logging.DEBUG)
    self.resource = False
    self.BIND_PYTHON(self.getName(), "__onLoad__", 0)
    self.BIND_PYTHON(self.getName(), "__onUnload__", 0)
    #always set autobind to true for the compatibility layer.
    #sometime BIND_PYTHON do not specify the number of arguments
    #that cant be guessed because the class is not provided to the method.
    autoBind = True
    if(autoBind):
      behName = self.getName()
      userMethList = set(dir(self)) - self._noNeedToBind
      for methName in userMethList:
        function = getattr(self, methName)
        if callable(function) and type(function) == type(self.__init__):
          if (methName[0] != "_"):  # private method
            self.functionName(methName, behName, "")
            for param in function.func_code.co_varnames:
              if (param != "self"):
                self.addParam(param)
            self._bindWithParam(behName, methName, _getMethodParamCount(function)-1)
    if brokerRegister:
      self.registerToBroker()

  def setParameterInternal(self, a, b):
      """ internal method used to call the good override for setParameter
          which can be overrided in user class. legacy hell.
      """
      self.setParameter(a, b)

  def session(self):
    return inaoqi.behavior.session(self)

  def __del__(self):
    NaoQiModule.__del__(self)
    self.logger.removeHandler(self.behaviorloghandler)
    self.behaviorloghandler.close()

  def __onLoad__(self):
    self._safeCallOfUserMethod("onLoad",None)

  def __onUnload__(self):
    if(self.resource):
        self.releaseResource()
    self._safeCallOfUserMethod("onUnload",None)

  def setParameter(self, parameterName, newValue):
    inaoqi.behavior.setParameter(self, parameterName, newValue)

  def _safeCallOfUserMethod(self, functionName, functionArg):
    import traceback
    try:
      if(functionName in dir(self)):
        func = getattr(self, functionName)
        if(func.im_func.func_code.co_argcount == 2):
          func(functionArg)
        else:
          func()
      return True
    except BaseException, err:
      if("onError" in dir(self)):
        try:
          self.onError(self.getName() + ':' + str(err))
        except BaseException, err2:
          self.logger.error(traceback.format_exc())
          self._reportError(self.behaviorId, self.__class__.__name__, traceback.format_exc())
      else:
        self.logger.error(traceback.format_exc())
        self._reportError(self.behaviorId, self.__class__.__name__, traceback.format_exc())
    return False

  # Depreciate this!!! Same as self.logger.info(), but function is always "log"
  def log(self, p):
    self.logger.info(p)


class MethodMissingMixin(object):
    """ A Mixin' to implement the 'method_missing' Ruby-like protocol. """
    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except:
            class MethodMissing(object):
                def __init__(self, wrapped, method):
                    self.__wrapped__ = wrapped
                    self.__method__ = method
                def __call__(self, *args, **kwargs):
                    return self.__wrapped__.method_missing(self.__method__, *args, **kwargs)

            return MethodMissing(self, attr)

    def method_missing(self, *args, **kwargs):
        """ This method should be overridden in the derived class. """
        raise NotImplementedError(str(self.__wrapped__) + " 'method_missing' method has not been implemented.")


class postType(MethodMissingMixin):
    def __init__(self):
        ""

    def setProxy(self, proxy):
        self.proxy = weakref.ref(proxy)
     #   print name

    def method_missing(self, method, *args, **kwargs):
          list = []
          list.append(method)
          for arg in args:
            list.append(arg)
          result = 0
          try:
                  p =  self.proxy()
                  result = p.pythonPCall(list)
          except RuntimeError,e:
                raise e

          return result



class ALProxy(inaoqi.proxy,MethodMissingMixin):

    def __init__(self, *args):
        self.post = postType()
        self.post.setProxy(self)
        if (len (args) == 1):
            inaoqi.proxy.__init__(self, args[0])
        elif (len (args) == 2):
            inaoqi.proxy.__init__(self, args[0],  args[1])
        else:
            inaoqi.proxy.__init__(self, args[0], args[1], args[2])

    def call(self, *args):
        list = []
        for arg in args:
            list.append(arg)

        return self.pythonCall(list)


    def pCall(self, *args):
        list = []
        for arg in args:
            list.append(arg)

        return self.pythonPCall(list)


    def method_missing(self, method, *args, **kwargs):
          list = []
          list.append(method)
          for arg in args:
            list.append(arg)
          result = 0
          try:
                result = self.pythonCall(list)
          except RuntimeError,e:
                raise e
                #print e.args[0]

          return result

    @staticmethod
    def initProxies():
        #Warning: The use of these default proxies is deprecated.
        global ALMemory
        global ALMotion
        global ALFrameManager
        global ALLeds
        global ALLogger
        global ALSensors
        try:
            ALMemory = inaoqi.getMemoryProxy()
        except:
            ALMemory = ALProxy("ALMemory")
        try:
            ALFrameManager = ALProxy("ALFrameManager")
        except:
            print "No proxy to ALFrameManager"
        try:
            ALMotion = ALProxy("ALMotion")
        except:
            print "No proxy to ALMotion"
        try:
            ALLeds = ALProxy("ALLeds")
        except:
            pass
        try:
            ALLogger = ALProxy("ALLogger")
        except:
            print "No proxy to ALLogger"
        try:
            ALSensors = ALProxy("ALSensors")
        except:
            pass


def createModule(name):
    global moduleList
    str = "moduleList.append("+ "module(\"" + name + "\"))"
    exec(str)
