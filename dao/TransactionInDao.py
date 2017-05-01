'''

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

def save(txIn, tx, index):
    deleteOld(tx, index)
    CoinSqlite3().exec_sql('INSERT INTO TransactionInfoIn(previous_hash, previous_index,script,sequence, parentBlockId,parentTxId,state,`index`) VALUES (?,?,?,?,?,?,?,?)', txIn.previous_hash, txIn.previous_index, txIn.script, txIn.sequence, tx.getBlockHash(), tx.hash(), txIn.state, index) 

def deleteOld(tx, index):   
    CoinSqlite3().exec_sql('Delete from TransactionInfoIn where parentBlockId = ? And parentTxId = ? And `Index` = ?', tx.getBlockHash(), tx.hash(), index)
