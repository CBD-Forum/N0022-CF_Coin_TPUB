'''

@author: Administrator
'''

import io
import time
import warnings

from pycoin.serialize import h2b
from pycoin.serialize.bitcoin_streamer import parse_struct
from pycoin.ui import standard_tx_out_script

import Constants
from dao import TransactionDao, TransactionOutDao, TransactionCFDao, \
    BlockchainDao, SecretKeyDao
from model.Transaction import Transaction
from model.TransactionCF import TransactionCF, CFHeader
from model.TransactionIn import TransactionIn
from model.TransactionOut import TransactionOut
# from socketInfo import SendMessage

def parse(f):
    tx_type, = parse_struct("L", f)
    if 0x01 == tx_type:
        tx = Transaction.parse(f)
    elif 0x02 == tx_type:
        tx = TransactionCF.parse(f)
    return tx

def from_bin(blob):
    """Return the Tx for the given binary blob."""
    f = io.BytesIO(blob)
    tx = parse(f)
    try:
        tx.parse_unspents(f)
    except Exception:
        # parsing unspents failed
        tx.unspents = []
    return tx

def from_hex(hex_string):
    """Return the Tx for the given hex string."""
    return from_bin(h2b(hex_string))

def tx_from_hex(hex_string):
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn("Call to deprecated function tx_from_hex, use from_hex instead",
                  category=DeprecationWarning, stacklevel=2)
    warnings.simplefilter('default', DeprecationWarning)
    return from_hex(hex_string)

# from pycoin.tx.pay_to import ScriptPayToAddressCFfrom pycoin.ui import standard_tx_out_sc
def insert(tx):
    if TransactionDao.isExist(tx):
        return
    
    if isCFTransation(tx):
        if TransactionDao.isPreCFlinked(tx):
            return
        if tx.cf_header.lack_amount <= 0:
            tx.cf_header.end_time = int(time.time())
    
    updatePreOutState(tx)         
    # 保存新交易
    TransactionDao.save(tx)
    
    # 如果是众筹成功 刷新所有众筹交易的状态为不可用
    if isCFTransation(tx):
        if tx.cf_header.lack_amount <= 0:
            TransactionDao.updateAllLinkedCFTransationOut(tx)
            TransactionOutDao.updateEndTimeToZero(tx)
            #把众筹初始发起的tx  usedstate设置为1
            TransactionDao.updateFirstCFState(tx)
    
def updatePreOutState(tx):
    # 更新已有交易状态
    for tx_in in tx.txs_in:
        TransactionOutDao.setStateUsed(tx_in.previous_hash, tx_in.previous_index)
    
def verify(transaction):
    isNotCFTx = True        
    # 如果输入小于输出，且不是最后一次众筹， 返回False                     
    if isCFTransation(transaction):
        if transaction.cf_header.lack_amount <= 0:      
            isNotCFTx = False
        
    # 脚本验证    
    # in对应的out是否存在，且没有被转出
    for tx_in in transaction.txs_in:
        if tx_in.is_coinbase:
            isNotCFTx = False;  
        else:  
            pre_tx_out = TransactionOutDao.searchByIndex(tx_in.previous_hash, tx_in.previous_index)
            if pre_tx_out == None:
                return False;
            if pre_tx_out.usedState == 1:
                return False;

    if isNotCFTx:
        return transaction.fee() >= 0
    else:        
        return True

def __get_tx_ins(pre_out_ids):
    pre_out_txs = []
    for pre_out_id in pre_out_ids:
        if '' != pre_out_id:
            pre_out_txs.append(TransactionOutDao.searchById(pre_out_id))
    tx_ins = []
    for pre_out_tx in pre_out_txs:
        script = b'' 
        sequence = 4294967295
        tx_in = TransactionIn(pre_out_tx.parent_hash, pre_out_tx.index, script, sequence, pre_out_tx.state)
        tx_ins.append(tx_in)
    return tx_ins

def __get_tx_outs(publicAddrToValueArray):
    tx_outs = []
    for singlePublicAddrToValueArray in publicAddrToValueArray:
        if len(singlePublicAddrToValueArray) == 2:
            value = singlePublicAddrToValueArray[1]
            script = standard_tx_out_script(singlePublicAddrToValueArray[0]);
            tx_out = TransactionOut(value, script, 0, 0)
            tx_outs.append(tx_out)
    return tx_outs
    
'''
    publicAddrToValue 字典  key 公钥地址  value数量
'''    

def createFirstTransaction(publicAddrToValueArray):
    tx_in = TransactionIn.coinbase_tx_in();
    tx_ins = []
    tx_ins.append(tx_in)
    tx_outs = __get_tx_outs(publicAddrToValueArray)
    
    tx = Transaction(Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME, None, 0)
    if verify(tx):
        insert(tx)
        # 广播新交易
        return tx

def createTransaction(pre_out_ids, publicAddrToValueArray):
    tx_ins = __get_tx_ins(pre_out_ids)
    tx_outs = __get_tx_outs(publicAddrToValueArray)
    
    tx = Transaction(Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME, None, 0)
    if verify(tx):
        insert(tx)
        # 广播新交易
        return tx

# 创建众筹交易块  新发起的众筹不进入此分支
def createNormalCFTransaction(pre_out_ids, pre_cf_hash, spendValue, otherPublicAddrToValueDict, refund_addr):
    tx_ins = __get_tx_ins(pre_out_ids)
    pre_cf = TransactionDao.searchByHash(pre_cf_hash);
    cf_header = pre_cf.cf_header
    cf_header.lack_amount = cf_header.lack_amount - spendValue
    cf_header.pre_hash = pre_cf_hash
    if cf_header.original_hash == '' or cf_header.original_hash == Constants.ZERO_HASH:
        cf_header.original_hash = pre_cf_hash
#     cfscript = b''
    if cf_header.lack_amount <= 0:#CF suceess
        outValue = cf_header.target_amount
        cfscript = standard_tx_out_script(cf_header.pubkey)
#     elif cf_header.lack_amount == cf_header.target_amount:#CF start
#         outValue = 0
#         cfscript = ScriptPayToAddress(refund_addr).script()
    else:#CF ing
        outValue = spendValue
        cfscript = standard_tx_out_script(refund_addr)
    #outValue = cf_header.target_amount if cf_header.lack_amount == 0 else spendValue
    cfout = TransactionOut(outValue, cfscript, 0, 0, cf_header.end_time)
    tx_outs = __get_tx_outs(otherPublicAddrToValueDict)
    tx_outs.insert(0, cfout)
    
    cf =  TransactionCF(cf_header, Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME, None, 0)
    if verify(cf):
        insert(cf)
        return cf
        
def createFirstCFTransaction(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee=[], cert=''):
    if len(pre_out_ids_for_fee) == 0:
        tx_in = TransactionIn.coinbase_tx_in();
        tx_ins = []
        tx_ins.append(tx_in)
    else:
        tx_ins = __get_tx_ins(pre_out_ids_for_fee)
    cert = SecretKeyDao.searchCertByPubAddr(pubkey_addr)
    cfscript = standard_tx_out_script(pubkey_addr)
    cfout = TransactionOut(0, cfscript, 0, 0, end_time)
    tx_outs = []
    tx_outs.append(cfout)
        
    original_hash = Constants.ZERO_HASH
    pre_hash = Constants.ZERO_HASH
    lack_amount = target_amount
    cf_header = CFHeader(original_hash, target_amount, pubkey_addr, end_time, pre_hash, lack_amount, cert)
    cf = TransactionCF(cf_header, Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME)
    if verify(cf):
        insert(cf)
        return cf

# 搜索指定hash的众筹交易，数组顺序为交易生成顺序。  state=0代表众筹未完成，state=1代表众筹完成
def searchCFTcsByOriginal_hash(original_hash):   
    return TransactionCFDao.searchCFTcsByOriginal_hash(original_hash)
            
def isCFTransation(tx):
    return isinstance(tx, TransactionCF)

def searchParentBlock(tx):
    blockHash = None
    if isinstance(tx, Transaction):
        blockHash = TransactionDao.searchParentBlockHash(tx)
    elif isinstance(tx, TransactionOut):
        blockHash = TransactionOutDao.searchParentBlockHash(tx)
    if blockHash == None:
        return None
    else:
        return BlockchainDao.search(blockHash)

# 判断out是否是众筹交易（index = 0 且父节点是cf）    
def isCFTransationOut(txout):
    #index不为0  肯定不是众筹
    if txout.index != 0:
        return False
    
    tx_hash = TransactionOutDao.searchParentTransactionHash(txout)
    tx = TransactionDao.searchByHash(tx_hash)
    if tx == None:
        return False
    else:
        return isCFTransation(tx)

# 通过寻找前一个out 获取in的pubAddress            
def getTxinPublicAddressByPre(txin):
    if txin.is_coinbase():
        return "(coinbase)"
    pre_tx = TransactionDao.searchByHash(txin.previous_hash)
    if pre_tx != None:
        pre_txout = pre_tx.txs_out[txin.previous_index];
        return pre_txout.address()
    else:
        return None

#支持tx和txout        
def getTransactionAndOutTime(tx):
    block = searchParentBlock(tx)
    if block == None:
        return int(time.time())
    else :
        return block.timestamp