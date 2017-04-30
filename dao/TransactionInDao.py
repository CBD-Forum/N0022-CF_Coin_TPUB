'''
Created on 2017��4��29��

@author: Administrator
'''

from dao.CoinSqlite3 import CoinSqlite3
from model.TransactionIn import TransactionIn


def search(parentBlockId, parentTxId):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoIn where parentBlockId = ? And parentTxId = ?', parentBlockId, parentTxId)
    txIns = []
    for tmp in c.fetchall():
        txIn = TransactionIn(tmp[1], tmp[2], tmp[3], tmp[4], tmp[7])
        txIns.append(txIn)
    return txIns

def save(txIn, tx):
    deleteOld(txIn, tx)
    CoinSqlite3().exec_sql('INSERT INTO TransactionInfoIn(previous_hash, previous_index,script,sequence, parentBlockId,parentTxId,state) VALUES (?,?,?,?,?,?,?)', txIn.previous_hash, txIn.previous_index, txIn.script, txIn.sequence, tx.block.hash(), tx.hash(), txIn.state)

def deleteOld(txIn, tx):   
    CoinSqlite3().exec_sql('Delete from TransactionInfoIn where parentBlockId = ? And parentTxId = ?', tx.block.hash(), tx.hash())
