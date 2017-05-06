'''
Created on 2017��4��29��

@author: Administrator
'''


from pycoin.tx.Spendable import Spendable

from dao import TransactionDao, SecretKeyDao
from dao.CoinSqlite3 import CoinSqlite3
from model.TransactionOut import TransactionOut
from utils import TransactionUtils


def searchAll():   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut')
    txOuts = []
    for tmp in c.fetchall():
        txOut = TransactionOut(tmp[1], tmp[2], tmp[5], tmp[9], tmp[10], tmp[0])
        txOuts.append(txOut)
    return txOuts

def searchById(id):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where id = ? ', id)
    tmp = c.fetchone()
    if tmp == None:
        return None
    else:    
        txOut = TransactionOut(tmp[1], tmp[2], tmp[5], tmp[9], tmp[10], tmp[0])
        return txOut

def searchSpendById(id):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where id = ? ', id)
    tmp = c.fetchone()
    spend = Spendable(tmp[1], tmp[2], tmp[4], tmp[6])
    return spend

def searchByIndex(parentTxId, index):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where parentTxId = ? And `index` = ?', parentTxId, index)
    tmp = c.fetchone()
    if tmp == None:
        return None
    else:    
        txOut = TransactionOut(tmp[1], tmp[2], tmp[5], tmp[9], tmp[10], tmp[0])
        return txOut

def search(parentBlockId, parentTxId):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where parentBlockId = ? And parentTxId = ?', parentBlockId, parentTxId)
    txOuts = []
    for tmp in c.fetchall():
        txOut = TransactionOut(tmp[1], tmp[2], tmp[5], tmp[9], tmp[10], tmp[0])
        txOuts.append(txOut)
    return txOuts  
  
def save(txOut, tx, index):
    deleteOld(tx, index)
    pubicAddress = txOut.address()
    end_time = 0
    if TransactionUtils.isCFTransation(tx):
        if 0 == index:
            end_time = tx.cf_header.end_time
    CoinSqlite3().exec_sql('INSERT INTO TransactionInfoOut(coin_value, script, parentBlockId, parentTxId, state, `index`, pubicAddress, isToMe, usedState, end_time) VALUES (?,?,?,?,?,?,?,?,?,?)', txOut.coin_value, txOut.script, tx.getBlockHash(), tx.hash(), txOut.state, index, pubicAddress, SecretKeyDao.isMypubicAddress(pubicAddress), 0, end_time)
  
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
def updateAllLinkedCFTransationOut(tx):
    c = CoinSqlite3().exec_sql('Select hash from TransactionInfo where original_hash = ?', tx.cf_header.original_hash)
    for tmp in c.fetchall():
        if tx.hash() != tmp[1]:
            CoinSqlite3().exec_sql('Update TransactionInfoOut set `usedState` = 1 where `parentTxId` = ? and `index` == 0', tmp[1])
  