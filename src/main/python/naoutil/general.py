'''
Created on Feb 8, 2013

@author: dsnowdon
'''

import sys
import inspect
import weakref


def class_to_name(klass):
    return klass.__name__

def object_to_name(obj):
    return obj.__class__.__name__

def object_to_FQCN(obj):
    return obj.__module__ + '.' + obj.__class__.__name__


'''
Remove class/function name to leave module name
'''
def FQCN_to_module(s):
    (moduleName, _) = split_FQCN(s)
    return moduleName

'''
Strip module name to leave class/function name
'''
def FQCN_to_class(s):
    (_, className) = split_FQCN(s)
    return className

'''
Split class name from module
'''
def split_FQCN(s):
    if '.' in s:
        return s.rsplit('.', 1)
    else:
        return (None, s)

'''
Look up a class from a FQCN
'''
def find_class(fqcn):
    (moduleName, className) = split_FQCN(fqcn)
    m = None
    if not moduleName is None:
        try:
            m = __import__(moduleName)
        except ImportError:
            print "Unable to import from {}".format(moduleName)
    
    #for name, obj in inspect.getmembers(m):
    for name, obj in inspect.getmembers(sys.modules[moduleName]):
        if inspect.isclass(obj) and className == name:
            return obj
        
    raise TypeError("Can't find class {}".format(fqcn))

def singleton(cls):
    '''
    Decorator for a class to transform it as a singleton.
    '''
    instances = weakref.WeakValueDictionary()
    def getinstance(*args):
        '''
        Lookup for the class in the weak dict and return its singleton instance.
        Called when creating an object.
        Do not recall __init__ with the new parameters.
        '''
        try:
            return instances[cls]
        except KeyError:
            instance = cls(*args) # Keep ref until we return it
            instances[cls] = instance
            return instance
    return getinstance
