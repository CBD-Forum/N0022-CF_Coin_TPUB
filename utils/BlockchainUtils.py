'''
# Created on 2017��4��29��

@author: Administrator
'''

import dao.BlockchainDao

def save(blockchain):
    return dao.BlockchainDao.save(blockchain)

def verify(blockchain):
    return True
    
def create(blockchain):
    save(blockchain)
    
    
