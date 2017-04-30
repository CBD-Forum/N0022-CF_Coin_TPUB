'''

@author: Administrator
'''
from dao import TransactionDao, TransactionOutDao
from model.TransactionOut import TransactionOut


def save(transaction):
    return TransactionDao.save(transaction)

def verify(transaction):
    #脚本验证    
    #in对应的out是否存在，且没有被转出
    for tx_in in transaction.txs_in:
        if tx_in.previous_hash != 0:
            pre_tx_out = TransactionOutDao.searchByIndex(tx_in.previous_hash, tx_in.previous_index)
            if pre_tx_out == None:
                return False;
            if pre_tx_out.usedState != 0:
                return False;
    return True
    
def create(transaction):
    save(transaction)
    
    