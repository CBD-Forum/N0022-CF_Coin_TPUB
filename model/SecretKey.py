'''
Created on 2017年5月1日

@author: Administrator
'''

class SecretKey(object):
    '''
    classdocs
    '''
    def __getPublicAdressFromKey__(self):
        return ""   

    def __init__(self, publicKey, privateKey=''):
        '''
        Constructor
        '''
        self.publicKey=publicKey;
        self.privateKey=privateKey;
        self.pubicAddress=self.getPublicAdressFromKey()
    