'''
Created on 2017年5月7日

@author: Administrator
'''
from socketInfo import SendMessage
from dao import TransactionDao
'''获取可用的out节点'''
'''造币交易'''

import time

from socketInfo.CoinSocket import ReivSocket
from utils import TransactionUtils


def createNewBitcoinTx(publicAddrToValueArray):
    return TransactionUtils.createFirstTransaction(publicAddrToValueArray)

'''生成普通交易'''
def createNormalBitCoinTx(pre_out_ids, publicAddrToValueArray):
    return TransactionUtils.createTransaction(pre_out_ids, publicAddrToValueArray);

'''生成普通众筹'''
def createNormalCFBitCoinTx(pre_out_ids, pre_cf_hash, spendValue, otherPublicAddrToValueDict, refund_addr):
    return TransactionUtils.createNormalCFTransaction(pre_out_ids, pre_cf_hash, spendValue, otherPublicAddrToValueDict, refund_addr);

'''生成新众筹'''
def createNewCFBitCoinTx(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee=[]):
    return TransactionUtils.createFirstCFTransaction(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee)


def test():
    tx = createNewBitcoinTx([['13DaZ9nfmJLfzU6oBnD2sdCiDmf3M5fmLx',12345]])
    tx = TransactionDao.searchByHash(tx.hash())
    tx2 = createNormalBitCoinTx([tx.txs_out[0].uid],[['1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd', 1230],['1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd', 1230], ['1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd', 10]]) 
    tx2 = TransactionDao.searchByHash(tx2.hash())   
    cf = createNewCFBitCoinTx(1000,'1DXNcbPEavwHQHtgPrjhkbG62f9SZBXp4v',2 * int(time.time()), [tx2.txs_out[2].uid])
    createNormalCFBitCoinTx([[tx2.txs_out[0].uid]], cf.hash(), 500, '1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd')
    createNormalCFBitCoinTx([[tx2.txs_out[1].uid]], cf.hash(), 500, '1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd')

if __name__ == '__main__':
    ReivSocket.init()
    SendMessage.initSendSocket()
    test() 