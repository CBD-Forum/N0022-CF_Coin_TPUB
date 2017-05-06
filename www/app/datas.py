import time


class WBlock():
    def __init__(self, id, height, hash, txs, timestamp, total, size):
        self.id = id
        self.height = height
        self.hash = hash
        self.txs = txs
        self.timestamp = timestamp
        self.total = total
        self.size = size
    def get_details(self):
        self.txs_number = 100
        self.fees = 12.2
        self.height = 125
        self.timestamp = time.time()
        self.difficulty = 0xffff001d
        self.size = 991.22
        self.version = 1
        self.nonce = 0x1548c5d1
        self.pre_hash = '0000000000000000014428af037a1fc0fd700d015d5d8a5f0dbd22d65f6ff906'
        self.next_hash = '00000000000000000188dbf31fcd76d13bd5abf60f3b7594963f765c153b909f'
        self.merkle_root = 'd69cefe09f87c9c461060b61007903d653322ba03e40b048f2387c327837a86a'
        tx = WTransaction()
        self.txs = [tx,]
class WTransaction():
    def __init__(self):
        self.tx_hash = '7d1eb678bc0a8d982b2a527c638afa714a08c6bf4b83f97be16967b23d8cc569'
        self.tx_inputs = ['1BK8VpXCgbBRvW7FqvgbsWZLW5kMV9Q8rW', '1GqRBaGo2babW4LJ4ipcQ5YC7PJ4wRzxfJ']
        self.tx_outputs = [['1PqbXjAadgPbvS8CmHLTC8HRkd7whiN5Te', 1.70251093],['1MT8cEhMf4oMiy2pAHKX2YWUH7AX2ep5t4 ', 0.01000184]]
        self.time = time.ctime()
        self.total_coin = 1.71251277
        self.fee = 0.12
  
class Key():
    def __init__(self, id):
        self.id = id
        self.pub_key = '1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF'
        self.sec_key = 'ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890'
        self.addr = '1234567890QWERTYUIOP'
        
def get_blocks():
    
    blocks = []
    blocks.append(WBlock(1, 3, '0000000000000000014428af037a1fc0fd700d015d5d8a5f0dbd22d65f6ff906', 2126, 1493706024, 298.2, 821.6 ))
    blocks.append(WBlock(2, 2, '0000000000000000034248af037a1fc0fd700d015d5d8a5f0dbd22d65f6ff906', 2054, 1493695806, 120.2, 900.5 ))
    blocks.append(WBlock(3, 1, '0000000000000000055768af037a1fc0fdabcdw15d5d8a5f0dbd22d65f6ff906', 1120, 1493620140, 200.5, 150.3 ))
    return blocks
   
def get_block_info(block_hash):
    block = WBlock(3, 1, '0000000000000000055768af037a1fc0fdabcdw15d5d8a5f0dbd22d65f6ff906', 1120, 1493620140, 200.5, 150.3 )
    block.get_details()
    return block

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