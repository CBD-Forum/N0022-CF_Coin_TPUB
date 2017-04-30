'''
# Created on 2017��4��29��

@author: Administrator
'''
import io
import json

from pycoin.serialize import b2h

from dao import BlockchainDao, NetNodeDao
from socketInfo import ConstantMessage
from socketInfo.CoinSocket import CoinSocket


def searchNetNodeMsg(addr):
#     ���Ͳ�ѯ�½ڵ�����
    message = json.dumps({"type":ConstantMessage.SEARCHNETNODEMSG})
    CoinSocket.sendMsg(message, addr)
    
def searchBlockMsg(id, addr):
#     ���Ͳ�ѯ�������� ids��Ϊ��Ϊָ������ Ϊ�ղ�ѯ����
    message = json.dumps({"type":ConstantMessage.SEARCHBLOCKMSG, "data":id})
    CoinSocket.sendMsg(message, addr)

def searchBlockMsgID(addr):
#     ���Ͳ�ѯ�������� ids��Ϊ��Ϊָ������ Ϊ�ղ�ѯ����
    message = json.dumps({"type":ConstantMessage.SEARCHBLOCKIDSMSG, "data":""})
    CoinSocket.sendMsg(message, addr)
    
def broadcastBlockMsg(block): 
#     ���͹�����������
    s = io.BytesIO()
    block.stream(s)
    block_as_hex = b2h(s.getvalue())
    message = json.dumps({"type":ConstantMessage.BROADCASTBLOCKMSG, "data":block_as_hex, "ttl":3})
    CoinSocket.broadcastMsg(message, NetNodeDao.searchAddrs())
    
def broadcastTransactionMsg(tx):    
    s = io.BytesIO()
    tx.stream(s)
    tx_as_hex = b2h(s.getvalue())
    message = json.dumps({"type":ConstantMessage.BROADCASTTRANSACTIONMSG, "data":tx_as_hex, "ttl":3})
    CoinSocket.broadcastMsg(message, NetNodeDao.searchAddrs())
