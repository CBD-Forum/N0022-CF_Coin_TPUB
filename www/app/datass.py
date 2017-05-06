
from dao import BlockchainDao, SecretKeyDao, TransactionDao
from utils import TransactionUtils


class WBlock():
    def __init__(self, block):
        self.id = block.uid
        self.height = block.height
        self.hash = block.hash()
        wtxs = []
        for tx in block.txs:
            wtxs.append(WTransaction(tx, block.timestamp))
        self.txs = wtxs
        self.timestamp = block.timestamp
        self.total = block.total_in()
        self.size = len(block.as_hex())
        
        self.txs_number = len(block.txs)
        self.fees = block.fee()
        self.height = block.height
        self.timestamp = block.timestamp
        self.difficulty = block.difficulty
        self.version = block.version
        self.nonce = block.nonce
        self.pre_hash = block.previous_block_hash
        self.next_hash = block.next_block_hash
        self.merkle_root = block.merkle_root

class WTransaction():
    def __init__(self, tx, timestamp=0):
        self.tx_hash = tx.hash().hex()
        inputs = []
        for txin in tx.txs_in:
            inputs.append(txin.address())
        self.tx_inputs = inputs
        outputs = []
        for txout in tx.txs_out:
            outputs.append([txout.address(), txout.coin_value])
        self.tx_outputs = outputs
        self.time = timestamp
        self.total_coin = tx.total_in()
        self.fee = tx.fee()
  
class Key():
    def __init__(self, secretKey):
        self.id = secretKey.uid
        self.pub_key = secretKey.publicKey
        self.sec_key = secretKey.privateKey
        self.addr = secretKey.pubicAddress
        
def get_blocks():    
    wblocks = []
    blocks = BlockchainDao.searchAll();
    for block in blocks:
        wblocks.append(WBlock(block))
    return wblocks
   
def get_block_info(block_hash):
    block = BlockchainDao.search(block_hash)
    wblock = WBlock(WBlock(block))
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