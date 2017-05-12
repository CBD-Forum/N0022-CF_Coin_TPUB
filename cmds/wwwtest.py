'''
Created on 2017年5月7日

@author: Administrator
'''
'''获取可用的out节点'''
'''造币交易'''

import time

from dao import TransactionDao
from socketInfo import SendMessage
from socketInfo.CoinSocket import ReivSocket, SendSocket
from utils import TransactionUtils


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
    return TransactionUtils.createFirstCFTransaction(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee, '''-----BEGIN CERTIFICATE-----
MIIDLjCCAhagAwIBAgIJAKTZkez5jH1vMA0GCSqGSIb3DQEBBQUAMG8xCzAJBgNV
BAYTAkNOMRAwDgYDVQQIDAdCZWlqaW5nMQ0wCwYDVQQKDARUUFVCMREwDwYDVQQL
DAhTZWN1cml0eTENMAsGA1UEAwwEdHB1YjEdMBsGCSqGSIb3DQEJARYOYWRtaW5A
dHB1Yi5jb20wHhcNMTcwNTA4MDgxMTEwWhcNMjcwNTA2MDgxMTEwWjBvMQswCQYD
VQQGEwJDTjEQMA4GA1UECAwHQmVpamluZzENMAsGA1UECgwEVFBVQjERMA8GA1UE
CwwIU2VjdXJpdHkxDTALBgNVBAMMBHRwdWIxHTAbBgkqhkiG9w0BCQEWDmFkbWlu
QHRwdWIuY29tMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEfStTpZiZKqNHJd2tYj/E
MOGYOxFrh/TTliVA3lXadzablXdB27YqBAQirbGnw+NJuvgxa7CBi/nMqahAMTnC
IGFBC/MLll7T4kS/f359/BiRbs4wMiuWNIzhoRugOAmgo3sweTAJBgNVHRMEAjAA
MCwGCWCGSAGG+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0ZTAd
BgNVHQ4EFgQUZ/QPXuhN9WaAjgAOUhOVNN1cELcwHwYDVR0jBBgwFoAUNUt6r4IA
A3nI7bjzFAXN2SRaapQwDQYJKoZIhvcNAQEFBQADggEBAMlXmy0e8a+KqUKZGW6P
+arugviHapt0QLUAxdFPPwbAQm7/wJYcbguAwPvxUQlHMsdvdSqEdDQeOYiOwft8
IGZ0dzNbynvhyH99tK42p5wgWRQyf4hMHrOnCdCgYUNOUVB0kPsSZ1R1ajSgfE/0
Xsi5Jbhpqpzm2G8NVqnPXeYfzQPZwzSgDs9INLs4Yw6aA8ei1IT8ESPSUtCSbFiT
HDB9G7UT/ZJBG6ZeGGONsf6ZOHZz38OkonBfL/tGS6NQzTFpr4H6yKyA3GlnYLOn
E+FOPdz0PSfhJOsKHY+AXFWPVrKfOimfznDYHpyQ0G6X9s31MAjF1JddRG6Xo1Vl
Ftg=
-----END CERTIFICATE-----
''')


def test():
    tx = createNewBitcoinTx([['13DaZ9nfmJLfzU6oBnD2sdCiDmf3M5fmLx',12345]])
    tx = TransactionDao.searchByHash(tx.hash())
    tx2 = createNormalBitCoinTx([tx.txs_out[0].uid],[['1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd', 1230],['1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd', 1230], ['1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd', 10]]) 
    tx2 = TransactionDao.searchByHash(tx2.hash())   
    cf = createNewCFBitCoinTx(1000,'1DXNcbPEavwHQHtgPrjhkbG62f9SZBXp4v',2 * int(time.time()), [tx2.txs_out[2].uid])
    cf2 = createNormalCFBitCoinTx([tx2.txs_out[0].uid], cf.hash(), 500, [[]],'1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd')
    createNormalCFBitCoinTx([tx2.txs_out[1].uid], cf2.hash(), 500, [[]], '1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd')

if __name__ == '__main__':
    SendSocket.init()
    test() 