'''

@author: Administrator
'''
import io
import json

from pycoin.serialize import b2h

from dao import BlockchainDao, NetNodeDao
from socketInfo import ConstantMessage
from socketInfo.CoinSocket import SendSocket


def searchNetNodeMsg(addr):
    message = json.dumps({"type":ConstantMessage.SEARCHNETNODEMSG})
    SendSocket.sendMsg(message, addr)
    
def searchBlockMsg(id, addr):
    message = json.dumps({"type":ConstantMessage.SEARCHBLOCKMSG, "data":id})
    SendSocket.sendMsg(message, addr)

def searchBlockMsgID(addr):
    message = json.dumps({"type":ConstantMessage.SEARCHBLOCKIDSMSG, "data":""})
    SendSocket.sendMsg(message, addr)
    
def broadcastBlockMsg(block): 
    s = io.BytesIO()
    block.stream(s)
    block_as_hex = b2h(s.getvalue())
    message = json.dumps({"type":ConstantMessage.BROADCASTBLOCKMSG, "data":block_as_hex, "ttl":3})
    SendSocket.broadcastMsg(message, NetNodeDao.searchAddrs())
    
def broadcastTransactionMsg(tx):    
    s = io.BytesIO()
    tx.stream(s)
    tx_as_hex = b2h(s.getvalue())
    message = json.dumps({"type":ConstantMessage.BROADCASTTRANSACTIONMSG, "data":tx_as_hex, "ttl":3})
    SendSocket.broadcastMsg(message, NetNodeDao.searchAddrs())
