'''
Created on 2017年4月30日

@author: Administrator

主方法   
1. 加载DB信息
2. 启动服务  开启监听
3. 像指定节点发请求，获取周边节点列表
4. 挖矿
'''
from time import sleep
import time

from pycoin.encoding import double_sha256
from pycoin.merkle import merkle
from pycoin.ui import standard_tx_out_script

import Constants
from dao import BlockchainDao, TransactionDao
from model import TransactionOut, Transaction
from model.Block import Block
from model.TransactionIn import TransactionIn
from socketInfo import SendMessage
from socketInfo.CoinSocket import ReivSocket, SendSocket


def findBlockChain():
    unchainedTxs = TransactionDao.searchUnChainedTx()  # 没有被打包的交易
    unlinkedBlock = BlockchainDao.searchUnlinkedBlock()  # 没被链接的区块
    
    version = Constants.VERSION
    timestamp = int(time.time())
    difficulty = Constants.DIFFICULTY
    txs = unchainedTxs
    
    minner_tx = insertFeeToMinner(txs)
    txs.insert(0, minner_tx) 
     
    state = 0
    if txs.__len__() == 0:
        merkle_root = 0
    else:
        merkle_root = merkle([tx.hash() for tx in txs], double_sha256)
        if 0 == merkle_root:
            return
    for block in unlinkedBlock: 
        previous_block_hash = block.hash()
        for nonce in range(0, 0xFFFFFFFF):
            tmpBlock = Block(version, previous_block_hash, merkle_root, timestamp, difficulty, nonce, txs, state)
            if tmpBlock.check_pow():
                for tx in tmpBlock.txs:
                    tx.block = tmpBlock                
                BlockchainDao.save(tmpBlock)
                SendMessage.broadcastBlockMsg(tmpBlock)

def insertFeeToMinner(txs):
    fee = 0;
    for tx in txs:
        fee += tx.fee()
    tx_in = TransactionIn.coinbase_tx_in(b'')
    tx_ins = []
    tx_ins.append(tx_in)
    
    
    script = standard_tx_out_script(Constants.MINNER_PUBADDR);
    tx_out = TransactionOut(fee, script, 0, 0)
    tx_outs = []
    tx_outs.append(tx_out)
    
    minner_tx = Transaction(Constants.VERSION, tx_ins, tx_outs, Constants.LOCK_TIME, None, 0) 
    return minner_tx
        
        
def main():
    ReivSocket()
    SendSocket.init()
    
#     addr = ('127.0.0.1', 8181)
#     SendMessage.searchNetNodeMsg(addr)   
    while True:
        findBlockChain()
        sleep(100)

if __name__ == '__main__':
    main()
