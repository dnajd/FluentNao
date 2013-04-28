'''
Created on Feb 10, 2013

@author: dsnowdon

Code used to abstract away some of the details of the NAOqi environment
so that clients do not need to pass around proxies and objects holding
loggers. Instead code justs passes around NaoEnvironment instances
'''
import inspect
import os

from naoqi import ALProxy

import i18n

SOURCE_DIR = "src"
RESOURCE_DIR = "resources"
DEFAULT_DATA_DIR_ROOT = "/home/nao"
DEFAULT_DATA_DIR_NAME = "data"

'''
The short names are the ones used to generate python properties, so you can use env.tts instead of
env.ALTextToSpeech
'''
PROXY_SHORT_NAMES = { 'audioDevice' : 'ALAudioDevice',
                      'audioLocalisation' : 'ALAudioSourceLocalisation',
                      'audioPlayer' : 'ALAudioPlayer',
                      'audioRecorder' : 'ALAudioRecoder',
                      'behaviourManager' : 'ALBehaviorManager',
                      'connectionManager' : 'ALConnectionManager',
                      'faceDetection' : 'ALFaceDetection',
                      'infrared' : 'ALInfrared',
                      'leds' : 'ALLeds',
                      'memory' : 'ALMemory',
                      'motion' : 'ALMotion',
                      'navigation' : 'ALNavigation',
                      'photoCapture' : 'ALPhotoCapture',
                      'preferences' : 'ALPreferences',
                      'resourceManager' : 'ALResourceManager',
                      'robotPosture' : 'ALRobotPosture',
                      'sensors' : 'ALSensors',
                      'sonar' : 'ALSonar',
                      'soundDetection' : 'ALSoundDetection',
                      'speechRecognition' : 'ALSpeechRecognition',
                      'tts' : 'ALTextToSpeech',
                      'videoDevice' : 'ALVideoDevice',
                      'videoRecorder' : 'ALVideoRecorder',
                      'visionRecognition' : 'ALVisionRecognition' }

'''
Hold information about the NAO environment and provide abstraction for logging
'''
# TODO build proxies on demand using python properties with custom getter
class NaoEnvironment(object):
    def __init__(self, box_, proxies={}, ipaddr=None, port=None):
        super(NaoEnvironment, self).__init__()
        self.box = box_
        self.app_name = None
        self.resources_path = None
        self.data_path = None
        self.proxyAddr = ipaddr
        self.proxyPort = port
        # construct the set of proxies, ensuring that we use only valid long names
        self.proxies = { }
        longNames = PROXY_SHORT_NAMES.values()
        for n, v in proxies.iteritems():
            if n in longNames:
                self.proxies[n] = v
            elif n in PROXY_SHORT_NAMES:
                self.proxies[PROXY_SHORT_NAMES[n]] = v
    
    def log(self, msg):
        self.box.log(msg)
    
    def _base_dir(self):
        this_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        prefix_end_index = this_dir.rindex(SOURCE_DIR)
        return this_dir[0:prefix_end_index]

    def application_name(self):
        return self.app_name
    
    def set_application_name(self, name):
        self.app_name = name

    def resources_dir(self):
        if self.resources_path is None:
            # if a path has not been set explicitly then find this path and replace everything
            # from src downwards with resources
            self.resources_path = os.path.join(self._base_dir(), RESOURCE_DIR)
        return self.resources_path
    
    def set_resources_dir(self, dir_name):
        self.resources_path = dir_name

    def data_dir(self):
        if self.data_path is None:
            if not self.application_name() is None:
                self.data_path = os.path.join(DEFAULT_DATA_DIR_ROOT, self.application_name())
            else:
                self.data_path = os.path.join(DEFAULT_DATA_DIR_ROOT, DEFAULT_DATA_DIR_NAME)
        # since, unlike the resources dir, the data dir is not part of the program it might not
        # already exist, so we create it if necessary
        if not os.path.exists(self.data_path):
            self.log('Creating data dir: '+self.data_path)
            try:
                os.makedirs(self.data_path)
            except OSError:
                self.log("Failed to creat dir: "+self.data_path)
        return self.data_path
    
    def set_data_dir(self, dir_name):
        self.data_path = dir_name
    
    def current_language(self):
        return self.tts.getLanguage()
    
    # return the two letter ISO language code for the current language
    def current_language_code(self):
        return i18n.language_to_code(self.current_language())
    
    def localized_text(self, basename, property_name):
        language_code = self.current_language_code()
        lt = i18n.get_property(self.resources_dir(), 
                               basename, 
                               language_code, 
                               property_name)
        self.log("Property '"+property_name+"' resolved to text '"+lt+"' in language '"+language_code+"'")
        return lt

    # read the named property from the specified config file. The file extension does not need
    # to be specified - both java style .properties & .json files will work 
    def get_property(self, basename, propertyName, defaultValue=None):
        dir_name = self.resources_dir()
        for ext in [i18n.EXT_PROPERTIES, i18n.EXT_JSON ]:
            filename = basename + ext
            path = dir_name + '/' + filename
            if os.path.exists(path):
                try:
                    props = i18n.read_properties_file(path)
                    contents = props[propertyName]
                    if isinstance(contents, basestring):
                        return contents.encode("utf-8").strip()
                    else:
                        return contents
                except KeyError:
                    # property was not found
                    return defaultValue
        # property file was not found
        return defaultValue

    # simulate having properties for all proxies without having to manually create each one
    def __getattr__(self, name):
        if name in PROXY_SHORT_NAMES or name in PROXY_SHORT_NAMES.values():
            # get the correct long name (key)
            key = name
            if name in PROXY_SHORT_NAMES:
                key = PROXY_SHORT_NAMES[name]
            
            if not key in self.proxies:
                self.add_proxy(key)
            
            return self.proxies[key]
        else:
            # not a valid short name or long name
            raise AttributeError

    # invoke ALProxy to create the proxy we need
    def add_proxy(self, longName):
        if self.proxyAddr and self.proxyPort:
            self.log('Creating proxy: ' + longName + " at "+self.proxyAddr+":"+str(self.proxyPort))
            self.proxies[longName] = ALProxy(longName, self.proxyAddr, self.portPort)
        else:
            self.log('Creating proxy: ' + longName)
            self.proxies[longName] = ALProxy(longName)

'''
Create environment object.
Needs to be called from a process with an ALBroker running (for example
within choreographe code)
'''
def make_environment(box_, proxies={}, ipaddr=None, port=None):
    return NaoEnvironment(box_, proxies, ipaddr, port)