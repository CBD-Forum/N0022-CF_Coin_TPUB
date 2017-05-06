
from dao import BlockchainDao


class WBlock():
    def __init__(self, id, block):
        self.id = id
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
    def __init__(self, tx, timestamp):
        self.tx_hash = tx.hash()
        inputs = []
#         for txin in tx.txs_in:
#             inputs.append(txin.address())
        self.tx_inputs = inputs
        outputs = {}
#         for txout in tx.txs_out:
#             outputs[txout.address()] = txout.value
        self.tx_outputs = outputs
        self.time = timestamp
        self.total_coin = tx.total_in()
        self.fee = tx.fee()
  
class Key():
    def __init__(self, id):
        self.id = id
        self.pub_key = '1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF'
        self.sec_key = 'ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890'
        self.addr = '1234567890QWERTYUIOP'
        
def get_blocks():    
    wblocks = []
    blocks = BlockchainDao.searchAll();
    iFlag = 0
    for block in blocks:
        ++iFlag
        wblocks.append(WBlock(++iFlag, block))
    return wblocks
   
def get_block_info(block_hash):
    block = BlockchainDao.search(block_hash)
    wblock = WBlock(WBlock(0, block))
    return wblock

def get_keys():
    keys = []
    for i in range(5):
        keys.append(Key(i))
    return keys

def get_my_txs():
    txs = []
    for i in range(5):
        txs.append(WTransaction())
    return txs