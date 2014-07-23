'''
Support for serialising python objects to JSON

Created on Mar 19, 2013

@author: dsnowdon
'''

import json

from general import object_to_FQCN, find_class

CLASS_TAG = '__class__'
VALUE_TAG = '__value__'

'''
Functions for clients to call to serialise/unserialise from strings and files

Idea taken from http://getpython3.com/diveintopython3/serializing.html 
and generalised to allow helper functions to be part of the custom classes
and avoid case statements
'''
def to_json_file(obj, fp):
    if not obj is None:
        json.dump(obj, fp, default=to_json_helper)

def to_json_string(obj):
    if obj is None:
        return ""
    else:
        return json.dumps(obj, default=to_json_helper)

def from_json_file(fp):
    return json.load(fp, object_hook=from_json_helper)

def from_json_string(sv):
    if sv is None or sv == "":
        return None
    else:
        return json.loads(sv, object_hook=from_json_helper)

'''
Convenience function to generate dictionary in correct format
'''
def object_to_json(obj, value):
    if value is None:
        return {CLASS_TAG: object_to_FQCN(obj) }
    else:
        return {CLASS_TAG: object_to_FQCN(obj),
                VALUE_TAG: value}

'''
Helper method to generate JSON for custom classes
'''
def to_json_helper(python_object):
    try:
        method = getattr(python_object, 'to_json')
        return object_to_json(python_object, method())
    except AttributeError:
        raise TypeError(repr(python_object) + ' is not JSON serializable')

'''
Helper function to detect serialized classes and call from_json on them
to regenerate the class
'''
def from_json_helper(json_object):
    # check whether this is an object we serialised and tagged with the class name
    if CLASS_TAG in json_object:
        fqcn = json_object[CLASS_TAG]
        klass = find_class(fqcn)

        # invoke from_json on target class
        try:
            try:
                json_object = getattr(klass, 'from_json')(json_object[VALUE_TAG])
            except KeyError:
                json_object = getattr(klass, 'from_json')(None)
        except AttributeError:
            # class does not support being reconstituted from JSON
            pass 
    return json_object
