'''
Created on 2017��4��29��

@author: Administrator
'''


import time

from pycoin.tx.Spendable import Spendable

from dao import SecretKeyDao
from dao.CoinSqlite3 import CoinSqlite3
from model.TransactionOut import TransactionOut
from utils import TransactionUtils


def searchAll():   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut')
    return __getSearchResult(c)

def __getSearchResult(c):
    txOuts = []
    for tmp in c.fetchall():
        txOut = TransactionOut(tmp[1], tmp[2], tmp[5], tmp[9], tmp[10], tmp[0], tmp[4], tmp[6])
        txOuts.append(txOut)
    return txOuts

def __getSearchResultSingle(c):
    tmp = c.fetchone()
    if tmp == None:
        return None
    else:    
        txOut = TransactionOut(tmp[1], tmp[2], tmp[5], tmp[9], tmp[10], tmp[0], tmp[4], tmp[6])
        return txOut
   
def searchMyTxOuts():
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where isMyTx = 1')
    return __getSearchResult(c)
   
def searchMyUnUsedNomalTxOuts():    #不包含未用的众筹交易
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where isMyTx = 1 and usedState = 0')
    return __getSearchResult(c)
   
def searchMyUnUsedTotalTxOuts():    #包含未成功的众筹交易
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where end_time < ? and usedState = 0', int(time.time()))
    return __getSearchResult(c)
 
def searchById(id):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where id = ? ', id)
    return __getSearchResultSingle(c);

def searchSpendById(id):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where id = ? ', id)
    tmp = c.fetchone()
    spend = Spendable(tmp[1], tmp[2], tmp[4], tmp[6])
    return spend

def searchByIndex(parentTxId, index):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where parentTxId = ? And `index` = ?', parentTxId, index)
    return __getSearchResultSingle(c);

def search(parentBlockId, parentTxId):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where parentBlockId = ? And parentTxId = ?', parentBlockId, parentTxId)
    return __getSearchResult(c)
  
def save(txOut, tx, index):
    deleteOld(tx, index)
    pubicAddress = txOut.address()
    end_time = 0
    if TransactionUtils.isCFTransation(tx):
        if 0 == index:
            end_time = tx.cf_header.end_time
    CoinSqlite3().exec_sql('INSERT INTO TransactionInfoOut(coin_value, script, parentBlockId, parentTxId, state, `index`, pubicAddress, isToMe, usedState, end_time, isMyTx) VALUES (?,?,?,?,?,?,?,?,?,?,?)', txOut.coin_value, txOut.script, tx.getBlockHash(), tx.hash(), txOut.state, index, pubicAddress, SecretKeyDao.isMypubicAddress(pubicAddress), 0, end_time, SecretKeyDao.isMypubicAddress(txOut.address()))
  
def updateState(tx_out, tx_out_id):
    CoinSqlite3().exec_sql('Update TransactionInfoOut set `usedState`=? where `id` = ?', tx_out.usedState, tx_out_id)
  
def setStateUsed(hash, index):
    CoinSqlite3().exec_sql('Update TransactionInfoOut set `usedState`=1 where `parentTxId` = ? and `index` = ?', hash, index)

def deleteOld(tx, index):   
    CoinSqlite3().exec_sql('Delete from TransactionInfoOut where parentBlockId = ? And parentTxId = ? And `Index` = ?', tx.getBlockHash(), tx.hash(), index)

"""create table if not exists TransactionInfoOut (
                id integer primary key,
                coin_value text not null,
                script text not null,
                parentBlockId text not null,
                parentTxId text not null,
                state text not null
                );"""

'''更新所有关联的out信息，设置状态为不可用'''
def updateAllLinkedCFTransationOut(hash):
    CoinSqlite3().exec_sql('Update TransactionInfoOut set `usedState` = 1 where `parentTxId` = ? and `index` = 0', hash)

def updateEndTimeToZero(tx):
    CoinSqlite3().exec_sql('Update TransactionInfoOut set `end_time`=0 where `parentTxId` = ?', tx.hash())
    
def searchParentBlockHash(txout):
    c = CoinSqlite3()._exec_sql('Select parentBlockId from TransactionInfoOut where `id` = ?', txout.uid)
    tmp = c.fetchone()
    if tmp == None:
        return None
    else:
        parentBlockId = tmp[0]
        return parentBlockId
    
def searchParentTransactionHash(txout):
    c = CoinSqlite3()._exec_sql('Select parentTxId from TransactionInfoOut where `id` = ?', txout.uid)
    tmp = c.fetchone()
    if tmp == None:
        return None
    else:
        parentTxId = tmp[0]
        return parentTxId