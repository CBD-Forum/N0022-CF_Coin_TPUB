'''
Created on 2017��4��29��

@author: Administrator
'''


from dao import TransactionDao
from dao.CoinSqlite3 import CoinSqlite3
from model.TransactionOut import TransactionOut


def search(parentBlockId, parentTxId):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfoOut where parentBlockId = ? And parentTxId = ?', parentBlockId, parentTxId)
    txOuts = []
    for tmp in c.fetchall():
        txOut = TransactionOut(tmp[1], tmp[2], tmp[5])
        txOuts.append(txOut)
    return txOuts
    
def save(txOut, tx, index):
    deleteOld(tx)
    CoinSqlite3().exec_sql('INSERT INTO TransactionInfoOut(coin_value, script, parentBlockId,parentTxId,state, `index`) VALUES (?,?,?,?,?,?)', txOut.coin_value, txOut.script, TransactionDao.getBlockHash(tx), tx.hash(), txOut.state, index)

def deleteOld(tx):   
    CoinSqlite3().exec_sql('Delete from TransactionInfoOut where parentBlockId = ? And parentTxId = ?', TransactionDao.getBlockHash(tx), tx.hash())

"""create table if not exists TransactionInfoOut (
                id integer primary key,
                coin_value text not null,
                script text not null,
                parentBlockId text not null,
                parentTxId text not null,
                state text not null
                );"""