'''

@author: Administrator
'''
from dao import TransactionInDao, TransactionOutDao
from dao.CoinSqlite3 import CoinSqlite3
from model.Transaction import Transaction
from model.TransactionCF import TransactionCF, CFHeader
from utils import TransactionUtils
import Constants

def __getSearchResult(c):
    txs = []
    for tmp in c.fetchall():
        parentBlockId = tmp[4]
        parentTxId = tmp[1]
        txs_in = TransactionInDao.search(parentBlockId, parentTxId)
        txs_out = TransactionOutDao.search(parentBlockId, parentTxId)
        if tmp[7] == 1:
            tx = Transaction(tmp[2], txs_in, txs_out, tmp[3], tmp[5].split(','), tmp[6], tmp[0])
        else:
            tx = TransactionCF(CFHeader(tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]), tmp[2], txs_in, txs_out, tmp[3], tmp[0])
        txs.append(tx)
        
    return txs

def __getSearchResultSingle(c):
    tmp = c.fetchone()
    parentBlockId = tmp[4]
    parentTxId = tmp[1]
    txs_in = TransactionInDao.search(parentBlockId, parentTxId)
    txs_out = TransactionOutDao.search(parentBlockId, parentTxId)
    if tmp[7] == 1:
        tx = Transaction(tmp[2], txs_in, txs_out, tmp[3], tmp[5].split(','), tmp[6], tmp[0])
    else:
        tx = TransactionCF(CFHeader(tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]), tmp[2], txs_in, txs_out, tmp[3], tmp[0])
        
    return tx

def searchAll():
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo')
    return __getSearchResult(c)
    

def search(parentBlockId):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where parentBlockId = ?', parentBlockId)
    return __getSearchResult(c)
    
    
def searchByHash(hash):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where hash = ?', hash)
    return __getSearchResultSingle(c)
    
def searchUnChainedTx():   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where parentBlockId = \'\'')
    return __getSearchResult(c)

# 搜索指定hash的众筹交易
def searchCFTcs(original_hash):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where original_hash = ?', original_hash)
    return __getSearchResult(c)
    
def save(tx):
    if isExist(tx):
        update(tx)
    else:
        insert(tx)

def insert(tx):
    if TransactionUtils.isCFTransation(tx):
        CoinSqlite3().exec_sql('INSERT INTO TransactionInfo(hash, version,lock_time,parentBlockId,unspents,state,type,original_hash, target_amount, pubkey, end_time, pre_hash, lack_amount) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', tx.hash(), tx.version, tx.lock_time, tx.getBlockHash(), ','.join(tx.unspents), tx.state, 2, tx.cf_header.original_hash, tx.cf_header.target_amount, tx.cf_header.pubkey, tx.cf_header.end_time, tx.cf_header.pre_hash, tx.cf_header.lack_amount)
    else:
        CoinSqlite3().exec_sql('INSERT INTO TransactionInfo(hash, version,lock_time,parentBlockId,unspents,state,type) VALUES (?,?,?,?,?,?,?)', tx.hash(), tx.version, tx.lock_time, tx.getBlockHash(), ','.join(tx.unspents), tx.state, 1)
        
    for index, txIn in enumerate(tx.txs_in):
        TransactionInDao.save(txIn, tx, index)
    for index, txOut in enumerate(tx.txs_out):
        TransactionOutDao.save(txOut, tx, index)  
          
def update(tx):
    if TransactionUtils.isCFTransation(tx):
        CoinSqlite3().exec_sql('Update TransactionInfo set `version`=?,`lock_time`=?,`parentBlockId`=?,`unspents`=?,`state`=?, `type` = ? ,original_hash = ?, target_amount = ?, pubkey = ?, end_time = ?, pre_hash = ?, lack_amount = ? where hash = ?', tx.version, tx.lock_time, tx.getBlockHash(), ','.join(tx.unspents), tx.state, 2, tx.cf_header.original_hash, tx.cf_header.target_amount, tx.cf_header.pubkey, tx.cf_header.end_time, tx.cf_header.pre_hash, tx.cf_header.lack_amount, tx.hash())
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

'''更新所有关联的out信息，设置状态为不可用'''
def updateAllLinkedCFTransationOut(tx):
    c = CoinSqlite3()._exec_sql('Select hash from TransactionInfo where original_hash = ?', tx.cf_header.original_hash)
    for tmp in c.fetchall():
        if tx.hash() != tmp[0]:
            TransactionOutDao.updateAllLinkedCFTransationOut(tmp[0])
            
def updateFirstCFState(tx):
#     CoinSqlite3()._exec_sql('Update TransactionInfo set `state`= 10 where hash = ?', tx.cf_header.original_hash)
    c = CoinSqlite3()._exec_sql('Select hash from TransactionInfo where hash = ?', tx.cf_header.original_hash)
    for tmp in c.fetchall():
        if tx.hash() != tmp[0]:
            TransactionOutDao.updateAllLinkedCFTransationOut(tmp[0])
    
def isPreCFlinked(cf):
    if cf.cf_header.pre_hash == '' or cf.cf_header.pre_hash == Constants.ZERO_HASH:
        return False
    else:
        c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where pre_hash = ?', cf.cf_header.pre_hash)
        s = c.fetchone()
        return s != None

        