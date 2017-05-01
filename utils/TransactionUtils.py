'''

@author: Administrator
'''
import time

from pycoin.tx import tx_utils
from pycoin.tx.Spendable import Spendable
from pycoin.tx.pay_to import ScriptPayToAddress
from pycoin.ui import standard_tx_out_script

import Constants
from dao import TransactionDao, TransactionOutDao
from model.Transaction import Transaction
from model.TransactionCF import TransactionCF
from model.TransactionIn import TransactionIn
from model.TransactionOut import TransactionOut
from socketInfo import SendMessage

ZERO_HASH = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def insert(tx):
    if TransactionDao.isExist(tx):
        return
    
    updatePreOutState(tx)         
    # 保存新交易
    TransactionDao.save(tx)
    
    # 如果是众筹成功 刷新所有众筹交易的状态为可用
    if isCFTransation(tx):
        if tx.cf_header.total == 0:
            TransactionOutDao.updateAllLinkedCFTransationOut(tx)
    
def updatePreOutState(tx):
    # 更新已有交易状态
    for tx_in in tx.txs_in:
        TransactionOutDao.setStateUsed(tx.hash(), tx_in.previous_index)
    
def verify(transaction):
    isNeedVerify = True        
    # 如果输入小于输出，且不是最后一次众筹， 返回False                     
    if isCFTransation(transaction):
        if transaction.cf_header.total == 0:      
            isNeedVerify = False
        
    # 脚本验证    
    pay = 0 
    # in对应的out是否存在，且没有被转出
    for tx_in in transaction.txs_in:
        if tx_in.previous_hash != ZERO_HASH:
            pre_tx_out = TransactionOutDao.searchByIndex(tx_in.previous_hash, tx_in.previous_index)
            if pre_tx_out == None:
                return False;
            if pre_tx_out.usedState == 1:
                return False;
            pay += pre_tx_out.coin_value
        else:
            isNeedVerify = False;
    for tx_out in transaction.txs_out:
        pay -= tx_out.coin_value       

    if isNeedVerify:
        return pay >= 0
    else:
        return True
        
def getPay(transaction):
    # 脚本验证    
    # in对应的out是否存在，且没有被转出
    pay = 0 
    for tx_in in transaction.txs_in:
        if tx_in.previous_hash != ZERO_HASH:
            pre_tx_out = TransactionOutDao.searchByIndex(tx_in.previous_hash, tx_in.previous_index)
            if pre_tx_out != None:
                pay += pre_tx_out.coin_value
    for tx_out in transaction.txs_out:
        pay -= tx_out.coin_value
    return pay


def __get_tx_ins(pre_out_ids):
    pre_out_txs = []
    for id in pre_out_ids:
        pre_out_txs.append(TransactionOutDao.searchById(id))
    tx_ins = []
    for pre_out_tx in pre_out_txs:
        script = b'' 
        sequence = 4294967295
        tx_in = TransactionIn(pre_out_tx.hash(), pre_out_tx.index, script, sequence, pre_out_tx.state)
        tx_ins.append(tx_in)
    return tx_ins

def __get_tx_outs(publicAddrToValueDict):
    tx_outs = []
    for publicAddr in publicAddrToValueDict.keys():
        value = publicAddrToValueDict[publicAddr]
        script = standard_tx_out_script(publicAddr);
        tx_out = TransactionOut(value, script, 0, 0)
        tx_outs.append(tx_out)
    return tx_outs
    
'''
    publicAddrToValue 字典  key 公钥地址  value数量
'''    

def createFirstTransaction(publicAddrToValueDict):
    tx_in = TransactionIn(ZERO_HASH, 4294967295)
    tx_ins = []
    tx_ins.append(tx_in)
    tx_outs = __get_tx_outs(publicAddrToValueDict)
    
    tx = Transaction(Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME, None, 0)
    if verify(tx):
        insert(tx)
        # 广播新交易
        SendMessage.broadcastTransactionMsg(tx)


def createTransaction(pre_out_ids, publicAddrToValueDict):
    tx_ins = __get_tx_ins(pre_out_ids)
    tx_outs = __get_tx_outs(publicAddrToValueDict)
    
    tx = Transaction(Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME, None, 0)
    if verify(tx):
        insert(tx)
        # 广播新交易
        SendMessage.broadcastTransactionMsg(tx)


def createCFTransaction(pre_out_ids, cf_header, spendValue, publicAddrToValueDict):
    tx_ins = __get_tx_ins(pre_out_ids)
    
    cfscript = b''
    outValue = cf_header.target_amount if cf_header.total == 0 else spendValue
    cfout = TransactionOut(outValue, cfscript, 0, 0, cf_header.end_time)
    tx_outs = __get_tx_outs(publicAddrToValueDict)
    tx_outs.insert(0, cfout)
    
    tx = Transaction(Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME, None, 0)
    if verify(tx):
        insert(tx)
        # 广播新交易
        SendMessage.broadcastTransactionMsg(tx)
            
def isCFTransation(tx):
    return isinstance(tx, TransactionCF)
