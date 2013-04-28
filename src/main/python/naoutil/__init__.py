'''
Created on March 19, 2013

@author: dsnowdon
@license: GNU LGPL v3
'''

import __main__
from naoqi import ALModule as _ALModule
from naoutil.general import object_to_FQCN

class ALModule(_ALModule):
    '''
    Wrap the original ALModule.
    Store the module in the globals directly.
    So you don't have to care about the rule 
    "The name given in the constructor must be the same as the variable name, which must be global".
    
    Also, you can just not supply any module name. One based on the fully qualified class name will be assigned to your module.
    If you need it later on, use self.moduleName.
    
    Just instanciate your module the way you want!
    
    @author: AxelVoitier
    Added on April 6, 2013
    '''
    def __init__(self, moduleName=None):
        if moduleName is None:
            moduleName = object_to_FQCN(self).replace('.', '_').lstrip('_')
        self.moduleName = str(moduleName)
        _ALModule.__init__(self, self.moduleName)
        setattr(__main__, self.moduleName, self)
