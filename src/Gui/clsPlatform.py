'''
Created on Jul 23, 2013

@author: stephanie
'''
import platform
class clsPlatform(object):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self.my_platform=platform.platform()
        self.OS = platform.system()
        
    @staticmethod    
    def get_slash():
        OS = platform.system()
        if OS == 'Darwin' or OS == 'mac':
            return '/'
        elif OS == 'Windows':
            return '\\'
        

    