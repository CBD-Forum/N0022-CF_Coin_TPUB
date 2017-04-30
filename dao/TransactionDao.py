'''
Created on 2017��4��29��

@author: Administrator
'''
from _overlapped import NULL

import Datacenter
from dao import TransactionInDao, TransactionOutDao


CoinSqlite3 = Datacenter.conn_

def search():   
    return NULL
    
def save():
    return NULL
    
def insertOrUpdate(tx):
    CoinSqlite3.execute("")
    for txIn in tx.txs_in:
        TransactionInDao.insertOrUpdate(txIn)
    for txOut in tx.txs_out:
        TransactionOutDao.insertOrUpdate(txOut)
    
