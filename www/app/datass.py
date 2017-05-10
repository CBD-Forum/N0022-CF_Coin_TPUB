
import time

from pycoin.serialize import h2b

from dao import BlockchainDao, SecretKeyDao, TransactionDao, TransactionInDao, \
    TransactionOutDao, TransactionCFDao
from utils import TransactionUtils, SecretKeyUtils

class WBlock():
    def __init__(self, block):
        self.id = block.uid
        self.height = block.height
        self.hash = block.hash()
        wtxs = []
        for tx in block.txs:
            wtxs.append(WTransaction(tx))
        self.txs = wtxs
        self.count_txs = len(self.txs)
        self.timestamp = time.ctime(block.timestamp)
        self.total = block.total_in()
        self.size = len(block.as_hex())
        
        self.txs_number = len(block.txs)
        self.fees = block.fee()
        self.height = block.height
        self.timestamp = time.ctime(block.timestamp)
        self.unix_time = block.timestamp
        self.difficulty = block.difficulty
        self.version = block.version
        self.nonce = block.nonce
        self.pre_hash = block.previous_block_hash
        self.next_hash = block.next_block_hash
        self.merkle_root = block.merkle_root

class WTransaction():
    def get_detail(self, tx):
        self.size = len(tx.as_hex()) #bytes
        block = TransactionUtils.searchParentBlock(tx)
        if block != None:
            self.block_hash = block.hash()
        else:
            self.block_hash = '1234567890asdfgh'
        self.in_amount = tx.total_in()
        self.fee_per_byte = float(self.fee / self.size) * 10**8
        self.in_scripts = ['1234567asdfxcvbn','123456ASDFGH']#这里怎么存看你方便
        self.out_scripts = []
        for txout in tx.txs_out:
            self.out_scripts.append(txout.script)
        
    def __init__(self, tx):
        self.tx_hash = tx.hash().hex()
        inputs = []
        for txin in tx.txs_in:
            inputs.append(TransactionUtils.getTxinPublicAddressByPre(txin))
        self.tx_inputs = inputs
        outputs = []
        for txout in tx.txs_out:
            if TransactionUtils.isCFTransationOut(txout):
                txout_type = '众筹交易'
            else:
                txout_type = '普通交易'
            outputs.append([txout.address(), txout.coin_value, txout_type, TransactionUtils.getTransactionAndOutTime(txout)])
        self.tx_outputs = outputs
        self.time = time.ctime(TransactionUtils.getTransactionAndOutTime(tx))
        self.total_coin = tx.total_in()
        self.fee = tx.fee()
        if TransactionUtils.isCFTransation(tx):
            self.tx_type = '众筹交易'
            self.lock_time = time.ctime(tx.cf_header.end_time)
        else:
            self.tx_type = '普通交易'
        self.get_detail(tx)
        
class Key():
    def __init__(self, secretKey):
        self.id = secretKey.uid
        self.pub_key = secretKey.publicKey
        self.sec_key = secretKey.privateKey
        self.addr = secretKey.pubicAddress

class CFProject():
    def __init__(self, cfs):
        if len(cfs) == 0:
            return
        src_cf = cfs[0]
        des_cf = cfs[-1]
        self.cf_id = src_cf.hash().hex()
        self.target_amount = src_cf.cf_header.target_amount
        self.start_time = time.ctime(TransactionUtils.getTransactionAndOutTime(src_cf)-3600*24*5)
        self.pubkey = src_cf.cf_header.pubkey
        self.end_time = time.ctime(src_cf.cf_header.end_time)
        self.lack_amount = des_cf.cf_header.lack_amount
        self.progress_rate = '%.2f %%' % ((des_cf.cf_header.target_amount - des_cf.cf_header.lack_amount) / des_cf.cf_header.target_amount *100)
        cert_obj = SecretKeyUtils.stringToCert(src_cf.cf_header.cert)
        self.cert = Cert(cert_obj)
        '''众筹成功，众筹失败'''
        if des_cf.cf_header.lack_amount <= 0:
            self.status = '众筹成功'
        elif src_cf.cf_header.end_time > int(time.time()):
            self.status = '正在进行'
        else:
            self.status = '众筹失败'   
                
        tmpPreCF = src_cf
        promoter = []
        for cf in cfs[1:]:
            promoter.append([cf.hash().hex(), TransactionUtils.getTransactionAndOutTime(cf), cf.txs_out[0].address(), tmpPreCF.cf_header.lack_amount - cf.cf_header.lack_amount])
            tmpPreCF = cf
        self.promoter = promoter
        self.process_date = [['day1',20], ['day2',30]]
#         self.cert = None
        
def get_blocks():    
    wblocks = []
    blocks = BlockchainDao.searchAll();
    for block in blocks:
        wblocks.append(WBlock(block))
    return wblocks
   
def get_block_info(block_hash):
    block = BlockchainDao.search(block_hash)
    wblock = WBlock(block)
    return wblock

def get_keys():
    secretKeys = SecretKeyDao.searchMySecrets()
    keys = []
    for secretKey in secretKeys:
        keys.append(Key(secretKey))
    return keys

def get_my_txs():
    txs = TransactionDao.searchAll()
#     for i in range(5):
#         txs.append(WTransaction())

    wtxs = []
    for tx in txs:
        wtxs.append(WTransaction(tx))
    return wtxs

def get_my_unused_in_txs():
    return TransactionInDao.searchMyUnUsedTxIns();

'''获取可用的out节点'''
def get_my_unused_out_txs():
    return TransactionOutDao.searchMyUnUsedTotalTxOuts();

'''造币交易'''
def createNewBitcoinTx(publicAddrToValueArray):
    return TransactionUtils.createFirstTransaction(publicAddrToValueArray)

'''生成普通交易'''
def createNormalBitCoinTx(pre_out_ids, publicAddrToValueArray):
    return TransactionUtils.createTransaction(pre_out_ids, publicAddrToValueArray);

'''生成普通众筹'''
def createNormalCFBitCoinTx(pre_out_ids, pre_cf_hash, spendValue, otherPublicAddrToValueArray, refund_addr):
    return TransactionUtils.createNormalCFTransaction(pre_out_ids, pre_cf_hash, spendValue, otherPublicAddrToValueArray, refund_addr);

'''生成新众筹'''
def createNewCFBitCoinTx(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee=[]):
    return TransactionUtils.createFirstCFTransaction(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee)

def get_CF_projects():
    allCFDict = TransactionCFDao.searchAllCFDict()
    projects = []
    for cfs in allCFDict.values():
        projects.insert(0, CFProject(cfs))
    return projects

def get_CF_project(project_id):
    allCFDict = TransactionCFDao.searchAllCFDict()
    cfs = allCFDict[h2b(project_id)]
    return CFProject(cfs)

class Cert():
    def __init__(self,cert_obj):
        self.issuer = cert_obj.get_issuer()  
        self.subject = cert_obj.get_subject()   
        self.expired = cert_obj.has_expired()
        self.notAfter = str(cert_obj.get_notAfter())[2:-1]
        self.notBefore = str(cert_obj.get_notBefore())[2:-1]
        self.serial_number = cert_obj.get_serial_number()
        self.signature_algorihm = str(cert_obj.get_signature_algorithm())[2:-1]
        
def get_tx(tx_id):
    tx = TransactionDao.searchByHash(tx_id)
    wtx = WTransaction(tx)
#     wtx.get_detail()
    return wtx

