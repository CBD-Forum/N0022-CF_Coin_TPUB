'''

@author: Administrator
'''
from dao import TransactionDao


def save(transaction):
    return TransactionDao.save(transaction)

def verify(transaction):
    return True
    
def create(transaction):
    save(transaction)
    
    