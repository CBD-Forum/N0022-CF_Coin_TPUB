'''

@author: Administrator
'''
from _overlapped import NULL
import io
import json

from pycoin.serialize import b2h, h2b

from dao import NetNodeDao, BlockchainDao, TransactionDao
from model.Block import Block
from model.NetNode import NetNode
from model.Transaction import Transaction
from utils import BlockchainUtils, TransactionUtils
from socketInfo import ConstantMessage
from socketInfo import CoinSocket
from _ast import If


def handleReceiMsg(message, addr):
    json_receive = json.loads(message)
    data = json_receive.get("data")
    type = json_receive.get("type")
    if(ConstantMessage.SEARCHNETNODEMSG == type):
        netNodes = NetNodeDao.searchAddrs()
#         replyData = [];  
#         for netNode in netNodes:
#             s = io.BytesIO()
#             netNode.stream(s)
#             netNode_as_hex = b2h(s.getvalue())
#             replyData.append(netNode_as_hex)
        
        json_reply = json.dumps({"data": netNodes, "type": ConstantMessage.REPLYNETNODEMSG})
        CoinSocket.SendSocket.sendMsg(json_reply, addr)
    elif(ConstantMessage.SEARCHBLOCKMSG == type):
        block = BlockchainDao.search(data)
        s = io.BytesIO()
        block.stream(s)
        block_as_hex = b2h(s.getvalue())        
        json_reply = json.dumps({"data": block_as_hex, "type":ConstantMessage.REPLYBLOCKMSG})
        CoinSocket.SendSocket.sendMsg(json_reply, addr)
    elif(ConstantMessage.SEARCHBLOCKIDSMSG == type):
        ids = BlockchainDao.searchIDs()
        json_reply = json.dumps({"data": ids, "type":ConstantMessage.REPLYBLOCKIDSMSG})
        CoinSocket.SendSocket.sendMsg(json_reply, addr)
    elif(ConstantMessage.BROADCASTBLOCKMSG == type):
        TTL = json_receive.get("ttl")
        block_as_hex = data
        block = Block.parse(io.BytesIO(h2b(block_as_hex)))
        if BlockchainUtils.verify(block):
            BlockchainUtils.insert(block)
        if TTL > 0:
            forwardMessage = json.dumps({"type":type, "data":data, "ttl":TTL - 1})
            CoinSocket.SendSocket.forward(forwardMessage, addr, NetNodeDao.searchAddrs())
    elif(ConstantMessage.BROADCASTTRANSACTIONMSG == type):
        TTL = json_receive.get("ttl")
        tx_as_hex = data
        tx = Transaction.parse(io.BytesIO(h2b(tx_as_hex)))
        if TransactionUtils.verify(tx):
            TransactionUtils.insert(tx)
        if TTL > 0:
            forwardMessage = json.dumps({"type":type, "data":data, "ttl":TTL - 1})
            CoinSocket.SendSocket.forward(forwardMessage, addr, NetNodeDao.searchAddrs())
    elif(ConstantMessage.REPLYNETNODEMSG == type): 
#         lstNetnode = []       
#         for netnode in data:
#             netNode = NetNode.parse(io.BytesIO(h2b(netnode_as_hex)))
#             NetNodeDao.save(netNode)
#             lstNetnode.append(netNode)
        return data  
    elif(ConstantMessage.REPLYBLOCKMSG == type):
        block = Block.parse(io.BytesIO(h2b(data)))
        if(BlockchainUtils.verify(block)):
            BlockchainUtils.insert(block)
        return block
    elif(ConstantMessage.REPLYBLOCKIDSMSG == type):
        return data
    else:
        pass        
    return

