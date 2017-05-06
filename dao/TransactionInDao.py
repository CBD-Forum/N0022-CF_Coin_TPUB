'''

@author: Administrator
'''

from dao.CoinSqlite3 import CoinSqlite3
from model.TransactionIn import TransactionIn
from dao import SecretKeyDao

def search(parentBlockId, parentTxId):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoIn where parentBlockId = ? And parentTxId = ?', parentBlockId, parentTxId)
    txIns = []
    for tmp in c.fetchall():
        txIn = TransactionIn(tmp[1], tmp[2], tmp[3], tmp[4], tmp[7], tmp[0])
        txIns.append(txIn)
    return txIns

def save(txIn, tx, index):
    deleteOld(tx, index)
    CoinSqlite3().exec_sql('INSERT INTO TransactionInfoIn(previous_hash, previous_index,script,sequence, parentBlockId,parentTxId,state,`index`, isMyTx) VALUES (?,?,?,?,?,?,?,?,?)', txIn.previous_hash, txIn.previous_index, txIn.script, txIn.sequence, tx.getBlockHash(), tx.hash(), txIn.state, index, SecretKeyDao.isMypubicAddress(txIn.address())) 

def deleteOld(tx, index):   
    CoinSqlite3().exec_sql('Delete from TransactionInfoIn where parentBlockId = ? And parentTxId = ? And `Index` = ?', tx.getBlockHash(), tx.hash(), index)

   
def searchMyTxIns():
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoIn where isMyTx = 1')
    txIns = []
    for tmp in c.fetchall():
        txIn = TransactionIn(tmp[1], tmp[2], tmp[3], tmp[4], tmp[7], tmp[0])
        txIns.append(txIn)
    return txIns
   
def searchMyUnUsedTxIns():
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoIn where isMyTx = 1 and usedState = 0')
    txIns = []
    for tmp in c.fetchall():
        txIn = TransactionIn(tmp[1], tmp[2], tmp[3], tmp[4], tmp[7], tmp[0])
        txIns.append(txIn)
    return txIns
 