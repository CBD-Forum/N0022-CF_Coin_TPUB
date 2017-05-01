'''

@author: Administrator
'''
from dao import TransactionInDao, TransactionOutDao
from dao.CoinSqlite3 import CoinSqlite3
from model.Transaction import Transaction
from model.TransactionCF import TransactionCF, CFHeader
from utils import TransactionUtils

def __getSearchResult(c):
    txs = []
    for tmp in c.fetchall():
        parentBlockId = tmp[3]
        parentTxId = tmp[0]
        txs_in = TransactionInDao.search(parentBlockId, parentTxId)
        txs_out = TransactionOutDao.search(parentBlockId, parentTxId)
        if tmp[6] == 1:
            tx = Transaction(tmp[1], txs_in, txs_out, tmp[2], tmp[4].split(','), tmp[5])
        else:
            tx = TransactionCF(CFHeader(tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12]), tmp[1], txs_in, txs_out, tmp[2])
        txs.append(tx)
        
    return txs

def search(parentBlockId):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where parentBlockId = ?', parentBlockId)
    return __getSearchResult(c)
    
def searchUnChainedTx():   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where parentBlockId = \'\'')
    return __getSearchResult(c)
    
def save(tx):
    if isExist(tx):
        update(tx)
    else:
        insert(tx)

def insert(tx):
    if TransactionUtils.isCFTransation(tx):
        CoinSqlite3().exec_sql('INSERT INTO TransactionInfo(hash, version,lock_time,parentBlockId,unspents,state,type,original_hash, target_amount, pubkey, end_time, pre_hash, total) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', tx.hash(), tx.version, tx.lock_time, tx.getBlockHash(), ','.join(tx.unspents), tx.state, 2, tx.cf_header.original_hash, tx.cf_header.target_amount, tx.cf_header.pubkey, tx.cf_header.end_time, tx.cf_header.pre_hash, tx.cf_header.total)
    else:
        CoinSqlite3().exec_sql('INSERT INTO TransactionInfo(hash, version,lock_time,parentBlockId,unspents,state,type) VALUES (?,?,?,?,?,?,?)', tx.hash(), tx.version, tx.lock_time, tx.getBlockHash(), ','.join(tx.unspents), tx.state, 1)
        
    for index, txIn in enumerate(tx.txs_in):
        TransactionInDao.save(txIn, tx, index)
    for index, txOut in enumerate(tx.txs_out):
        TransactionOutDao.save(txOut, tx, index)  
          
def update(tx):
    if TransactionUtils.isCFTransation(tx):
        CoinSqlite3().exec_sql('Update TransactionInfo set `version`=?,`lock_time`=?,`parentBlockId`=?,`unspents`=?,`state`=?, `type` = ? ,original_hash = ?, target_amount = ?, pubkey = ?, end_time = ?, pre_hash = ?, total = ? where hash = ?', tx.version, tx.lock_time, tx.getBlockHash(), ','.join(tx.unspents), tx.state, 2, tx.cf_header.original_hash, tx.cf_header.target_amount, tx.cf_header.pubkey, tx.cf_header.end_time, tx.cf_header.pre_hash, tx.cf_header.total, tx.hash())
    else:    
        CoinSqlite3().exec_sql('Update TransactionInfo set `version`=?,`lock_time`=?,`parentBlockId`=?,`unspents`=?,`state`=?, `type` = ? where hash = ?', tx.version, tx.lock_time, tx.getBlockHash(), ','.join(tx.unspents), tx.state, 1, tx.hash())

    for index, txIn in enumerate(tx.txs_in):
        TransactionInDao.save(txIn, tx, index)
    for index, txOut in enumerate(tx.txs_out):
        TransactionOutDao.save(txOut, tx, index)  
                
def isExist(tx):
    tmp = CoinSqlite3()._exec_sql('Select * from TransactionInfo where hash = ?', tx.hash())
    s = tmp.fetchone()
    return s != None
