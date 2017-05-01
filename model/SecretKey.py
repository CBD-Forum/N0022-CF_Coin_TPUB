'''
Created on 2017年5月1日

@author: Administrator
'''
from pycoin.key import Key


class SecretKey(object):
    '''
    classdocs
    '''

    def __init__(self, publicKey, privateKey=''):
        '''
        Constructor
        '''
        self.publicKey=publicKey;
        self.privateKey=privateKey;
        if '' != privateKey:            
            self.key_obj = Key(public_pair=[publicKey, privateKey])
            self.pubicAddress = self.key_obj.address()
    
    @classmethod    
    def create(cls, sec_num):
        key_obj = Key(secret_exponent=sec_num)
        publicKey, privateKey = key_obj._public_pair
        return cls(publicKey, privateKey)
#         self.pubicAddress = key_obj.address()
#         self.key_obj = key_obj
