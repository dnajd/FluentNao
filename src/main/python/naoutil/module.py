'''
Created on April 06, 2013

@author: AxelVoitier
@license: GNU LGPL v3
'''

import __main__

from naoqi import ALModule

from naoutil.general import object_to_FQCN

class Module(ALModule):
    '''
    Wrap the original ALModule.
    Store the module in the globals directly.
    So you don't have to care about the rule 
    "The name given in the constructor must be the same as the variable name, which must be global".
    
    Also, you can just not supply any module name. One based on the fully qualified class name will be assigned to your module.
    If you need it later on, use self.moduleName.
    
    Just instanciate your module the way you want!
    '''
    def __init__(self, module_name=None):
        if module_name is None:
            module_name = object_to_FQCN(self).replace('.', '_').lstrip('_')
        self.module_name = str(module_name)
        ALModule.__init__(self, self.module_name)
        setattr(__main__, self.module_name, self)
