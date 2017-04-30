'''
# Created on 2017��4��29��

@author: Administrator
'''
from _ast import If
from _overlapped import NULL

import Datacenter
from dao import TransactionDao, CoinSqlite3
from dao.CoinSqlite3 import CoinSqlite3


def search():   
    return NULL
              
def searchIDs():   
    return NULL

def searchByID(id):   
    return NULL

# def save(blockChain):    
#     pass

def insert(blockChain):
    CoinSqlite3().exec_sql('INSERT INTO BlockInfo(hash, version,previous_block_hash,merkle_root,timestamp,difficulty,nonce,state) VALUES (?,?,?,?,?,?,?,?)', blockChain.hash(), blockChain.version, blockChain.previous_block_hash, blockChain.merkle_root, blockChain.timestamp, blockChain.difficulty, blockChain.nonce, blockChain.state)
#     for tx in blockChain.txs:
#         TransactionDao.insertOrUpdate(tx)
        
def update(blockChain):
    CoinSqlite3().exec_sql('Update BlockInfo set `version`=?,`previous_block_hash`=?,`merkle_root`=?,`timestamp`=?,`difficulty`=?,`nonce`=?,`state`=? where hash = ?', blockChain.version, blockChain.previous_block_hash, blockChain.merkle_root, blockChain.timestamp, blockChain.difficulty, blockChain.nonce, blockChain.state, blockChain.hash())
#     for tx in blockChain.txs:
#         TransactionDao.insertOrUpdate(tx)
        
def isExist(blockChain):
    tmp = CoinSqlite3()._exec_sql('Select * from BlockInfo where hash = ?', blockChain.hash())
    s = tmp.fetchone()
    return s != None
    

def save(blockChain):    
    if isExist(blockChain):
        update(blockChain)
    else:
        insert(blockChain)
