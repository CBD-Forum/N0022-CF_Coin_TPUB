'''

@author: Administrator
'''
from dao import TransactionDao, TransactionOutDao
from model.TransactionOut import TransactionOut
from model.TransactionIn import TransactionIn
from model.Transaction import Transaction
import Constants
from socketInfo import SendMessage


def insert(tx):
    if TransactionDao.isExist(tx):
        return
    
    updatePreOutState(tx)         
    #保存新交易
    TransactionDao.save(tx)
    
def updatePreOutState(tx):
    #更新已有交易状态
    for tx_in in tx.txs_in:
        TransactionOutDao.setStateUsed(tx_in.hash(), tx_in.index)
    
def verify(transaction):
    # 脚本验证    
    pay = 0 
    # in对应的out是否存在，且没有被转出
    for tx_in in transaction.txs_in:
        if tx_in.previous_hash != 0:
            pre_tx_out = TransactionOutDao.searchByIndex(tx_in.previous_hash, tx_in.previous_index)
            if pre_tx_out == None:
                return False;
            if pre_tx_out.usedState != 0:
                return False;            
            pay += pre_tx_out.coin_value
    for tx_out in transaction.txs_out:
        pay -= tx_out.coin_value       
                        
    # 如果输入小于输出 返回False        
    return pay >= 0

def getPay(transaction):
    # 脚本验证    
    # in对应的out是否存在，且没有被转出
    pay = 0 
    for tx_in in transaction.txs_in:
        if tx_in.previous_hash != 0:
            pre_tx_out = TransactionOutDao.searchByIndex(tx_in.previous_hash, tx_in.previous_index)
            if pre_tx_out != None:
                pay += pre_tx_out.coin_value
    for tx_out in transaction.txs_out:
        pay -= tx_out.coin_value
    return pay
    
'''
    publicAddrToValue 字典  key 公钥地址  value数量
'''    
def createTransaction(pre_out_ids, publicAddrToValueDict):
    pre_out_tx_dict = {}
    for id in pre_out_ids:
        pre_out_tx_dict[id]=TransactionOutDao.searchById(id)
        
    tx_ins = []
    for pre_out_tx in pre_out_tx_dict.values():
        script = b'' 
        sequence = 4294967295
        tx_in = TransactionIn(pre_out_tx.hash(), pre_out_tx.index, script, sequence, pre_out_tx.state)
        tx_ins.append(tx_in)
    
    tx_outs = []
    for publicAddr in publicAddrToValueDict.keys():
        value = publicAddrToValueDict[publicAddr]
        script = '';
        tx_out = TransactionOut(value, script, 0, 0)
        tx_outs.append(tx_out)
    
    tx = Transaction(Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME, None, 0)
    
    if verify(tx):
        insert(tx)
        #广播新交易
        SendMessage.broadcastTransactionMsg(tx)
            
    