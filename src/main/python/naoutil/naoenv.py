'''
Created on Feb 10, 2013

@author: dsnowdon

Code used to abstract away some of the details of the NAOqi environment
so that clients do not need to pass around proxies and objects holding
loggers. Instead code just passes around NaoEnvironment instances
'''
import inspect
import os
import logging

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
PROXY_SHORT_NAMES = { 'animatedSpeech': 'ALAnimatedSpeech',
                      'audioDevice' : 'ALAudioDevice',
                      'audioLocalisation' : 'ALAudioSourceLocalisation',
                      'audioPlayer' : 'ALAudioPlayer',
                      'audioRecorder' : 'ALAudioRecoder',
                      'alife' : 'ALAutonomousLife',
                      'behaviourManager' : 'ALBehaviorManager',
                      'connectionManager' : 'ALConnectionManager',
                      'dialog' : 'ALDialog',
                      'faceDetection' : 'ALFaceDetection',
                      'faceTracker' : 'ALFaceTracker',
                      'ballTracker' : 'ALRedBallTracker',
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
class NaoEnvironment(object):
    def __init__(self, box_, proxies={}, ipaddr=None, port=None):
        super(NaoEnvironment, self).__init__()
        self.box = box_
        self.app_name = None
        self.resources_path = None
        self.data_path = None
        self.proxyAddr = ipaddr
        self.proxyPort = port
        self.logger = logging.getLogger("naoutil.naoenv.NaoEnvironment")
        # construct the set of proxies, ensuring that we use only valid long names
        self.proxies = { }
        longNames = PROXY_SHORT_NAMES.values()
        for n, v in proxies.iteritems():
            if n in longNames:
                self.proxies[n] = v
            elif n in PROXY_SHORT_NAMES:
                self.proxies[PROXY_SHORT_NAMES[n]] = v

    # equivalent to logging at info level but also allows fallback to choreographe box
    # and print statements
    def log(self, msg):
        if self.box:
            self.box.log(msg)
        elif self.logger:
            self.logger.info(msg)
        else:
            print msg

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
            self.logger.debug('Creating data dir: {}'.format(self.data_path))
            try:
                os.makedirs(self.data_path)
            except OSError:
                self.logger.error("Failed to create dir: {}".format(self.data_path))
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
        self.logger.debug("Property '{name}' resolved to text '{value}' in language '{lang}'"
                          .format(name=property_name, value=lt, lang=language_code))
        return lt

    # read the named property from the specified config file. The file extension does not need
    # to be specified - both java style .properties & .json files will work
    def get_property(self, basename, propertyName, defaultValue=None):
        dir_name = self.resources_dir()
        for ext in [i18n.EXT_PROPERTIES, i18n.EXT_JSON ]:
            filename = basename + ext
            path = os.path.join(dir_name, filename)
            if i18n.get_from_cache(path) or os.path.exists(path):
                try:
                    props = i18n.read_properties_file_with_cache(path)
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

    # invoke ALProxy to store the proxy we need
    def add_proxy(self, longName):
        self.proxies[longName] = self.create_proxy(longName)

    # invoke ALProxy to create the proxy we need
    def create_proxy(self, longName):
        if self.proxyAddr and self.proxyPort:
            self.logger.debug('Creating proxy: {name} at {proxy.proxyAddr}:{proxy.proxyPort}'.format(name=longName, proxy=self))
            return ALProxy(longName, self.proxyAddr, self.proxyPort)
        else:
            self.logger.debug('Creating proxy: {name}'.format(name=longName))
            return ALProxy(longName)

'''
Create environment object.
Needs to be called from a process with an ALBroker running (for example
within choreographe code)
'''
def make_environment(box_, proxies={}, ipaddr=None, port=None):
    return NaoEnvironment(box_, proxies, ipaddr, port)
