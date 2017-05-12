
import time

from numpy import random
from pycoin.serialize import h2b

from dao import BlockchainDao, SecretKeyDao, TransactionDao, TransactionInDao, \
    TransactionOutDao, TransactionCFDao
from socketInfo import SendMessage
from utils import TransactionUtils, SecretKeyUtils


class WBlock():
    def __init__(self, block):
        self.block = block
        self.id = block.uid
        self.height = block.height
        self.hash = block.hash()
        self.count_txs = len(block.txs)
        self.timestamp = time.ctime(block.timestamp)
        self.total = block.total_in()
        self.size = len(block.as_hex())
        
        self.txs_number = len(block.txs)
        
        self.height = block.height
        self.timestamp = time.ctime(block.timestamp)
        self.unix_time = block.timestamp
        
    
    def get_details(self):
        wtxs = []
        for tx in self.block.txs:
            wtxs.append(WTransaction(tx))
        self.txs = wtxs
        self.count_txs = len(self.txs)
        self.fees = self.block.fee()
        self.difficulty = self.block.difficulty
        self.version = self.block.version
        self.nonce = self.block.nonce
        self.pre_hash = self.block.previous_block_hash
        self.next_hash = self.block.next_block_hash
        self.merkle_root = self.block.merkle_root

class WTransaction():
    def get_detail(self, tx):
        self.size = len(tx.as_hex()) #bytes
        block = TransactionUtils.searchParentBlock(tx)
        if block != None:
            self.block_hash = block.hash()
        else:
            self.block_hash = 'None'
        self.in_amount = tx.total_in()
        self.fee_per_byte = float(self.fee / self.size) * 10**8
        rand = random.randint(13)
        in_scripts = ['304402200f851e44a303c01203a9efce71b8472a53a69b0866795a613e8a18511fb7f9ad022054dc6a354462bf29d1128e064c30fb269ead454f59fbdc4c1a24736748cc9aed0102213c8e5d43845c0708fea710b0e6428b469bb4ac375ad278a408d8ee8f6657cf',
                      '3045022100cd775627ea6ade0afcd7f2c621364686ce9e042a272b52dcddb110a742c4935102207046f05acec413c7cb31865e3411b926526c6231a4f29fb81b2c1c6f60738e5f010238e4a226145abe843ab470b3de2a1817020d8904b8040e85147e565c749fd2f7',
                      '30440220314ad635a036190c7a62bae7b847c1ff3a9c0b0667ec1b887a256de412c4c706022061fccece187c4ab0ab80361e831189f225f4734c43ea171c41ce483f5316f1220103311914b86112e25397a2497b9df45c40646bf2bc480bfd1fb7b4ef896426eeed',
                      '3045022100a41e45f2ef79bd3c85856d1ceec66d5a9c4255cca11fff4ae6ed2190230a527a02207a166a12211b5923facd8074b247a95c75ff7c78bcbd0200b6d681017d739d4e010330304ee875117e0a05b1e3930bc59b258c81cba236c0211cb55bee199270dc8a',
                      '304402203324f7e5cd7755659385dfccfecb58a5c1ea9e4010820c7988e507b9b550e0a30220432ff43e1bf14137fa6963ee7585f7bdb294c2e27abb1386c2f59ec70df957000103fda0bce81384163131ac2f998d54039786f13d2638cc373b90926f0b5b8be729',
                      '3045022100c9a884fec8fc25466c909601669fddc962c677069edd29af2a6814c399e106c20220579c80222bf754fd9b0886d1c1526070270166bb331492e66200bddf990b48b00103953a097c80665ca0d4721f7849d93b023c83afa793b705cf1015d77f94f952c4',
                      '304402206d5d8ffbbc77541a7240485c948b024ec933bd822593979c41ca1c9259ba8acf02203ce5e63ed3753219510263ad0a95119a579c23aaf8ed9e47cd91b82f66e4b1b7010244f0e6eb11d9847fc0806b21606ce134dd049c821bc93bc3759c1102e745bca6',
                      '30440220584fbdaa9ebbc64602b82977cacfe6a7da6a732a1c1c5b3003c3114f564babcc02201f8b81d15522d4faacf74da423516d624def15ee7dbb009b0589912491fc306601034629a351f6f513ba4234ea33e6791e3debc062902e6d8e03317da15915fdc480',
                      '3045022100a009f847590f6d075d8342f82388cbd53c360a7b39306f2550c2afbaca1484e802205f61a41351df6e5314d3c1c4783aebae1dd4cbd3110c4a1b8a3316548441f2a101028c053c34abd8a1eb1b81989f75443a63188e19f4817ab2d461e6f9ea5f6e833c',
                      '3045022100ce236387d8f4649be174c2b8e9f6e7a1e8032d2f29a0e95019f2f3202d5d6ec002207367219e5741fc19e95e05b4ec2c6b0fc64bab39025482f1975e464867e5b7bb01027461abd36ded728717cd42131f4b67a2e5e4603bb49b3b85fe2aab4cf8ea33eb',
                      '30450221008a4c926bc0656c10fd09724a7f6198db32125182a6d8f2a72a6b6a215789c3a8022019b615f1eae9ba6303ac07fb0ed60e7450e0a11976a8d5bd7f66417e7a51528c01031f9bf0f18b3435dfd72734547ccb07d56adbb89e8b0202fb832a5f99386970b3',
                      '3044022054562f435edb7286e563c7323e140125c9b99d92f0ed1cf644923f45891e5f1d02206a858c828710f9905a7ae085a955d9c2074f521354672662c251e891c02d492d0103b947c83d61cb6e25da0b3564cf85377b803fb80c0ca86d99d429bb7ad2d2aa87',
                      '3045022100ae1eb6de01c7c51fc098fa03f4c229628452a06be52a6d7e1077898f4dfaa26902206443c3e98d7c0c46432f9ce993a9977436ee948cf4f070ea42fbbbb8270924af0103d4bbe6bbf74befb298a6629ac48f363524afb5773ea556d323cbf665032824aa'
                      ]
        self.in_scripts = []#这里怎么存看你方便
        for i in range(len(self.tx_inputs)):
            self.in_scripts.append(in_scripts[random.randint(13)])
        
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
            outputs.append([txout.address(), txout.coin_value, txout_type, TransactionUtils.getTransactionAndOutTime(txout), txout.usedState])
        self.tx_outputs = outputs
        self.time = time.ctime(TransactionUtils.getTransactionAndOutTime(tx))
        self.total_coin = tx.total_in()
        self.fee = tx.fee()
        if TransactionUtils.isCFTransation(tx):
            self.tx_type = '众筹交易'
            self.lock_time = time.ctime(tx.cf_header.end_time)
            self.pre_hash = tx.cf_header.pre_hash.hex()
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
        self.cfs = cfs
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
        
        if src_cf.cf_header.cert not in ('', None):
            cert_obj = SecretKeyUtils.stringToCert(src_cf.cf_header.cert)
            self.cert = Cert(cert_obj)
        else:
            self.cert = None
        '''众筹成功，众筹失败'''
        if des_cf.cf_header.lack_amount <= 0:
            self.status = '众筹成功'
        elif src_cf.cf_header.end_time > int(time.time()):
            self.status = '正在进行'
        else:
            self.status = '众筹失败'   
                
    def get_details(self):
        src_cf = self.cfs[0]
        des_cf = self.cfs[-1]
        tmpPreCF = src_cf
        promoter = []
        for cf in self.cfs[1:]:
            promoter.append([cf.hash().hex(), time.ctime(TransactionUtils.getTransactionAndOutTime(cf)), cf.txs_out[0].address(), tmpPreCF.cf_header.lack_amount - cf.cf_header.lack_amount])
            tmpPreCF = cf
        self.promoter = promoter
        self.process_date = [['day1',20], ['day2',30]]
        
def get_blocks():    
    wblocks = []
    blocks = BlockchainDao.searchAll();
    for block in blocks:
        wblocks.append(WBlock(block))
    return wblocks
   
def get_block_info(block_hash):
    block = BlockchainDao.search(block_hash)
    wblock = WBlock(block)
    wblock.get_details()
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
    tx_ins = TransactionInDao.searchMyUnUsedTxIns();
    for tx_in in tx_ins:
        tx_in.addr = TransactionUtils.getTxinPublicAddressByPre(tx_in)
    return tx_ins
    

'''获取可用的out节点'''
def get_my_unused_out_txs():
    tx_outs = TransactionOutDao.searchMyUnUsedTotalTxOuts();
    for tx_out in tx_outs:
        tx_hash = TransactionOutDao.searchParentTransactionHash(tx_out)
        tx = TransactionDao.searchByHash(tx_hash)
        in_addr = []
        for tx_in in tx.txs_in:
            in_addr.append(TransactionUtils.getTxinPublicAddressByPre(tx_in))
        tx_out.in_addr = in_addr
        if TransactionUtils.isCFTransationOut(tx_out):
            txout_type = '众筹交易'
        else:
            txout_type = '普通交易'
        tx_out.type = txout_type
    return tx_outs    

'''造币交易'''
def createNewBitcoinTx(publicAddrToValueArray):
    if len(publicAddrToValueArray) == 0:
        return None
    tx = TransactionUtils.createFirstTransaction(publicAddrToValueArray)
    if tx != None:
        SendMessage.broadcastTransactionMsg(tx)
    return tx

'''生成普通交易'''
def createNormalBitCoinTx(pre_out_ids, publicAddrToValueArray):
    if len(pre_out_ids) == 0 or len(publicAddrToValueArray) == 0:
        return None
    tx = TransactionUtils.createTransaction(pre_out_ids, publicAddrToValueArray);
    if tx != None:
        SendMessage.broadcastTransactionMsg(tx)
    return tx

'''生成普通众筹'''
def createNormalCFBitCoinTx(pre_out_ids, pre_cf_hash, spendValue, otherPublicAddrToValueArray, refund_addr):
    if len(pre_out_ids) == 0:
        return None
    cf = TransactionUtils.createNormalCFTransaction(pre_out_ids, pre_cf_hash, spendValue, otherPublicAddrToValueArray, refund_addr);
    if cf != None:
        SendMessage.broadcastTransactionMsg(cf)
    return cf

'''生成新众筹'''
def createNewCFBitCoinTx(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee=[]):
    cf = TransactionUtils.createFirstCFTransaction(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee)
    if cf != None:
        SendMessage.broadcastTransactionMsg(cf)
    return cf

def get_CF_projects():
    allCFDict = TransactionCFDao.searchAllCFDict()
    projects = []
    for cfs in allCFDict.values():
        projects.insert(0, CFProject(cfs))
    return projects

def get_CF_project(project_id):
    allCFDict = TransactionCFDao.searchAllCFDict()
    cfs = allCFDict[h2b(project_id)]
    project = CFProject(cfs)
    project.get_details()
    return project

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

