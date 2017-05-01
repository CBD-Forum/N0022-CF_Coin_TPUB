'''

@author: Administrator
'''

from dao import BlockchainDao
from utils import TransactionUtils

def verify(blockchain):
    for tx in blockchain.txs:
        if not TransactionUtils.verify(tx):
            return False
    return True
       
def insert(blockchain):
    if BlockchainDao.isExist(blockchain):
        return
    
    for tx in blockchain.txs:
        TransactionUtils.updatePreOutState(tx)
    
    BlockchainDao.save(blockchain)
    