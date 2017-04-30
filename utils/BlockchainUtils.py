'''

@author: Administrator
'''

import dao.BlockchainDao
from utils import TransactionUtils

def save(blockchain):
    return dao.BlockchainDao.save(blockchain)

def verify(blockchain):
    for tx in blockchain.txs:
        if not TransactionUtils.verify(tx):
            return False
    return True
    
def create(blockchain):
    save(blockchain)
    
    
