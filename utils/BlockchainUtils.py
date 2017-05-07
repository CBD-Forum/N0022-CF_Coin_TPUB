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
    
    if BlockchainDao.isPreBlockLinked(blockchain):  #如果前一个区块被链接了  则失效
        return
    
    for tx in blockchain.txs:
        TransactionUtils.updatePreOutState(tx)
    
    BlockchainDao.save(blockchain)
    