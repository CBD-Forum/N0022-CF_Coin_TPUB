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
    
    if len(unchainedTxs) == 0 or len(unlinkedBlock) == 0:
        return
    
    version = Constants.VERSION
    timestamp = int(time.time())
    difficulty = Constants.DIFFICULTY
    txs = unchainedTxs
    for tx in txs:
        if tx.fee() > 0:
            feeOut = getFeeOut(tx.fee())
            tx.txs_out.append(feeOut)
     
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

def getFeeOut(fee):
    script = standard_tx_out_script(Constants.MINNER_PUBADDR);
    coin_value = fee
    txout = TransactionOut.TransactionOut(coin_value, script)
    return txout
        
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
