'''
Created on 21/4/2012

@author: David Snowdon (c) 2012
'''

import codecs
import os

import jprops
import json

# Map language names from TTS to ISO language code
# ISO language codes from http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes        
LANGUAGE_MAP = {
                "arabic" : "ar",
                "brazilian" : "pt",
                "chinese" : "zh",
                "czech" : "cs",
                "dutch" : "nl",
                "danish" : "da",
                "english" : "en",
                "filipino" : "tl",
                "Finnish" : "fi",
                "french" : "fr",
                "german" : "de",
                "italian" : "it",
                "japanese" : "ja",
                "korean" : "ko",
                "Polish" : "pl",
                "portuguese" : "pt",
                "russian" : "ru",
                "spanish" : "es",
                "swedish" : "sv",
                "turkish" : "tr"
                }

DEFAULT_ENCODING = "utf-8"

DEFAULT_LANGUAGE_CODE = "en"

EXT_PROPERTIES = ".properties"
EXT_JSON = ".json"
EXT_TEXT = ".txt"

def language_to_code(languageName):
    global LANGUAGE_MAP
    return LANGUAGE_MAP[languageName.lower()]

def check_language_code(language_code):
    # attempt to detect whether language is the two-letter ISO code or
    # the language name
    global DEFAULT_LANGUAGE_CODE
    if language_code is None:
        language_code = DEFAULT_LANGUAGE_CODE
    else:
        if len(language_code) > 2:
            language_code = language_to_code(language_code)
    return language_code.lower()

def make_filename(basename, language_code, ext):
    return basename + "_" + language_code + ext

def find_resource(dir_name, basename, language_code, exts):
    """
        First try the requested language and if that file does not exist
        try the default language.
    """
    global DEFAULT_LANGUAGE_CODE
    # first try with requested language
    for ext in exts:
        filename = make_filename(basename, language_code, ext)
        path = dir_name + '/' + filename
        if os.path.exists(path):
            return path
    
    # now try with default language
    for ext in exts:
        filename = make_filename(basename, DEFAULT_LANGUAGE_CODE, ext)
        path = dir_name + '/' + filename
        if os.path.exists(path):
            return path
        
    return None

def read_text_file(filename, encoding="utf-8"):
    with codecs.open(filename, encoding=encoding) as fp:
        contents = fp.read()
        result = contents.encode("utf-8")
    return result

def read_properties_file(filename, encoding="utf-8"):
    with codecs.open(filename, encoding=encoding) as fp:
        if filename.endswith(EXT_PROPERTIES):
            properties = jprops.load_properties(fp)
        else:
            properties = json.load(fp)
    return properties

def read_text_options(dir_name, basename, language_code, property_name=None, separator='/'):
    """
        Gets a list of text options to choose from for the appropriate language
        Can handle being given a language name or two letter ISO code.
        Separator is used when splitting a property, for files newline
        is used as a separator.
    """
    global EXT_PROPERTIES
    global EXT_TEXT
    global EXT_JSON
    language_code = check_language_code(language_code)
    if property_name is None:
        # should be a plain text file with one option per line
        path = find_resource(dir_name, basename, language_code, [ EXT_TEXT ])
        contents = read_text_file(path)
        return contents.strip().split('\n')
    else:
        # should be a properties or JSONfile
        path = find_resource(dir_name, basename, language_code, [EXT_PROPERTIES, EXT_JSON ])
        if not path is None:
            props = read_properties_file(path)
            value = props[property_name]
            # if we loaded from JSON this will already be a list
            if isinstance(value, basestring):
                contents = value.strip()
                contents = contents.encode("utf-8")
                return contents.split(separator)
            else:
                contents = []
                for x in value:
                    contents.append(x.strip().encode("utf-8"))
                return contents
        else:
            return None

def get_property(dir_name, basename, language_code, property_name):
    """
        Read a localized value from a property file
    """
    global EXT_PROPERTIES
    language_code = check_language_code(language_code)
    path = find_resource(dir_name, basename, language_code, [ EXT_PROPERTIES, EXT_JSON ])
    if not path is None:
        props = read_properties_file(path)
        contents = props[property_name].strip()
        return contents.encode("utf-8")
    else:
        return None
    