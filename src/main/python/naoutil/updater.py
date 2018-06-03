'''
Created on September 01, 2013

@author: AxelVoitier
@license: GNU LGPL v3

Provide helper functions to update or checkout a source code base from DevProg
or GithHub repositories.
'''
import os
import subprocess

def update_code_base(path, repository=None, refspec=None):
    '''
    Execute a git pull on the given path.
    It can be any path, not just naoutil code base.

    Throw a subprocess.CalledProcessError in case of error from git.
    
    Simply use like:
    naoutil.updater.update_code_base('.')
    or
    naoutil.updater.update_code_base('./src/main/python/myThirdParty')
    '''
    cwd = os.getcwd()
    try:
        os.chdir(path)
        cmd = ['git', 'pull']
        if repository:
            cmd.append(repository)
        
        if refspec:
            try:
                cmd += refspec
            except TypeError:
                cmd.append(refspec)
                
        subprocess.check_call(cmd)
    finally:
        os.chdir(cwd)
