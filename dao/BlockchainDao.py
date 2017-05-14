'''
# Created on 2017��4��29��

@author: Administrator
'''
from _ast import If
import os
import traceback

from dao import TransactionDao
from dao.CoinSqlite3 import CoinSqlite3
from model.Block import Block
import Constants

def __sort_txs(txs):
    sort_txs = []
    for tx in txs:
        if len(tx.txs_in) == 1 and tx.txs_in[0].is_coinbase() and 0 == tx.fee():
            sort_txs.insert(0,tx)
        else:
            sort_txs.append(tx)
    return sort_txs
            

def search(hash):       
    c = CoinSqlite3()._exec_sql('Select * from BlockInfo where hash = ?', hash)
    tmp = c.fetchone()
    if tmp != None:
        txs = TransactionDao.search(hash)
        sort_txs = __sort_txs(txs)
        block = Block(tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], sort_txs, tmp[8], tmp[9], tmp[10], tmp[0])
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
        sort_txs = __sort_txs(txs)
        block = Block(tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], sort_txs, tmp[8], tmp[9], tmp[10], tmp[0])
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
        
    writeBlock(blockChain)


def writeBlock(blockChain):
    try:
        fileParentPath = Constants.FILEPATH
        filename = fileParentPath + str(blockChain.hash().hex()) + '.bin'
        if not os.path.exists(fileParentPath):
            os.mkdir(fileParentPath)
        if os.path.exists(filename):
            os.remove(filename)
        output = open(filename, 'wb')
        output.close
        output = open(filename, 'wb')
        blockChain.stream(output)
        output.close
    except:  
        traceback.print_exc() 