'''
# Created on 2017��4��29��

@author: Administrator
'''
from _ast import If

from dao import TransactionDao
from dao.CoinSqlite3 import CoinSqlite3
from model.Block import Block


def search(hash):       
    c = CoinSqlite3()._exec_sql('Select * from BlockInfo where hash = ?', hash)
    tmp = c.fetchone()
    if tmp != None:
        txs = TransactionDao.search(hash)
        block = Block(tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], txs, tmp[8], tmp[9], tmp[10], tmp[0])
        for tx in txs:
            tx.block = block
        return block
              
def searchIDs():   
    c = CoinSqlite3()._exec_sql('Select previous_block_hash from BlockInfo')
    hashs = []
    for tmp in c.fetchall():
        hashs.append(tmp[1])
    return hashs

def searchAll(): 
    c = CoinSqlite3()._exec_sql('Select * from BlockInfo')
    blocks = []
    for tmp in c.fetchall():
        txs = TransactionDao.search(tmp[1])
        block = Block(tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], txs, tmp[8], tmp[9], tmp[10], tmp[0])
        for tx in txs:
            tx.block = block
        blocks.append(block)
    return blocks

def searchUnlinkedBlock(): 
    c = CoinSqlite3()._exec_sql('Select previous_block_hash from BlockInfo')
    preBlockHashs = []
    for tmp in c.fetchall():
        preBlockHashs.append(tmp[0])

    blocks = searchAll()    
    unlinkedBlocks = []    
    for block in blocks:
        if block.hash() not in preBlockHashs:
            unlinkedBlocks.append(block)
    return unlinkedBlocks

# def save(blockChain):    
#     pass

def __insert(blockChain, preHeight):
    CoinSqlite3().exec_sql('INSERT INTO BlockInfo(hash, version,previous_block_hash,merkle_root,timestamp,difficulty,nonce,state,height) VALUES (?,?,?,?,?,?,?,?,?)', blockChain.hash(), blockChain.version, blockChain.previous_block_hash, blockChain.merkle_root, blockChain.timestamp, blockChain.difficulty, blockChain.nonce, blockChain.state, preHeight + 1)
    for tx in blockChain.txs:
        TransactionDao.save(tx)

def __updatePreBlock(blockChain):
    CoinSqlite3().exec_sql('Update BlockInfo set `next_block_hash` =? where hash = ?', blockChain.hash(), blockChain.previous_block_hash)    
        
def __update(blockChain, preHeight):
    CoinSqlite3().exec_sql('Update BlockInfo set `version`=?,`previous_block_hash`=?,`merkle_root`=?,`timestamp`=?,`difficulty`=?,`nonce`=?,`state`=?,`height`=? where hash = ?', blockChain.version, blockChain.previous_block_hash, blockChain.merkle_root, blockChain.timestamp, blockChain.difficulty, blockChain.nonce, blockChain.state, preHeight + 1, blockChain.hash())
    for tx in blockChain.txs:
        TransactionDao.save(tx)
        
def isExist(blockChain):
    tmp = CoinSqlite3()._exec_sql('Select * from BlockInfo where hash = ?', blockChain.hash())
    s = tmp.fetchone()
    return s != None

def isPreBlockLinked(blockChain):
    tmp = CoinSqlite3()._exec_sql('Select * from BlockInfo where previous_block_hash = ?', blockChain.previous_block_hash)
    s = tmp.fetchone()
    return s != None

def save(blockChain):  
    preBlock = search(blockChain.previous_block_hash)  
    if preBlock == None:
        preHeight = 0;
    else:
        preHeight = preBlock.height;
    if isExist(blockChain):
        __update(blockChain, preHeight)
    else:
        __insert(blockChain, preHeight)
    
    if preBlock != None:    
        __updatePreBlock(blockChain)
