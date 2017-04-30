'''

@author: Administrator
'''
from dao import TransactionInDao, TransactionOutDao
from dao.CoinSqlite3 import CoinSqlite3
from model.Transaction import Transaction

def search(parentBlockId):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where parentBlockId = ?', parentBlockId)
    txs = []
    for tmp in c.fetchall():
        parentBlockId = tmp[3]
        parentTxId = tmp[0]
        txs_in = TransactionInDao.search(parentBlockId, parentTxId)
        txs_out = TransactionOutDao.search(parentBlockId, parentTxId)
        tx = Transaction(tmp[1], txs_in, txs_out, tmp[2], tmp[4].split(','), tmp[5])
        txs.append(tx)
        
    return txs
    
def searchUnChainedTx():   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where parentBlockId = \'\'')
    txs = []
    for tmp in c.fetchall():
        parentBlockId = tmp[3]
        parentTxId = tmp[0]
        txs_in = TransactionInDao.search(parentBlockId, parentTxId)
        txs_out = TransactionOutDao.search(parentBlockId, parentTxId)
        tx = Transaction(tmp[1], txs_in, txs_out, tmp[2], tmp[4].split(','), tmp[5])
        txs.append(tx)
        
    return txs
    
def save(tx):
    if isExist(tx):
        update(tx)
    else:
        insert(tx)

def getBlockHash(tx):
    if hasattr(tx, 'block'):
        return tx.block.hash()
    else:
        return ''

def insert(tx):
    CoinSqlite3().exec_sql('INSERT INTO TransactionInfo(hash, version,lock_time,parentBlockId,unspents,state) VALUES (?,?,?,?,?,?)', tx.hash(), tx.version, tx.lock_time, getBlockHash(tx),','.join(tx.unspents),tx.state)
    for txIn in tx.txs_in:
        TransactionInDao.save(txIn, tx)
    for txOut in tx.txs_out:
        TransactionOutDao.save(txOut, tx)  
              
def update(tx):
    CoinSqlite3().exec_sql('Update TransactionInfo set `version`=?,`lock_time`=?,`parentBlockId`=?,`unspents`=?,`state`=? where hash = ?', tx.version, tx.lock_time, getBlockHash(tx), ','.join(tx.unspents), tx.state, tx.hash())
    for txIn in tx.txs_in:
        TransactionInDao.save(txIn, tx)
    for txOut in tx.txs_out:
        TransactionOutDao.save(txOut, tx)  
                
def isExist(tx):
    tmp = CoinSqlite3()._exec_sql('Select * from TransactionInfo where hash = ?', tx.hash())
    s = tmp.fetchone()
    return s != None
