'''

@author: Administrator
'''
from _overlapped import NULL
import io
import json

from pycoin.serialize import b2h, h2b

from socketInfo import CoinSocket
from dao import NetNodeDao, BlockchainDao
from model.Block import Block
from model.NetNode import NetNode
from model.Transaction import Transaction
from utils import BlockchainUtils, TransactionUtils
from socketInfo import ConstantMessage


def handleReceiMsg(message, addr):
    json_receive = json.loads(message.decode("utf8"))
    data = json_receive.get("data")
    type = json_receive.get("type")
    if(ConstantMessage.SEARCHNETNODEMSG == type):
        netNodes = NetNodeDao.search()
        replyData = [];  
        for netNode in netNodes:
            s = io.BytesIO()
            netNode.stream(s)
            netNode_as_hex = b2h(s.getvalue())
            replyData.append(netNode_as_hex)
        
        json_reply = json.dump({"data": replyData, "type": ConstantMessage.REPLYBLOCKMSG})
        CoinSocket.CoinSocket.sendMsg(json_reply, addr)
    elif(ConstantMessage.SEARCHBLOCKMSG == type):
        block = BlockchainDao.search(data)
        s = io.BytesIO()
        block.stream(s)
        block_as_hex = b2h(s.getvalue())        
        json_reply = json.dump({"data": block_as_hex, "type":ConstantMessage.REPLYBLOCKMSG})
        CoinSocket.CoinSocket.sendMsg(json_reply, addr)
    elif(ConstantMessage.SEARCHBLOCKIDSMSG == type):
        ids = BlockchainDao.searchIDs()
        json_reply = json.dump({"data": ids, "type":ConstantMessage.REPLYBLOCKIDSMSG})
        CoinSocket.CoinSocket.sendMsg(json_reply, addr)
    elif(ConstantMessage.BROADCASTBLOCKMSG == type):
        TTL = json_receive.get("ttl")
        block_as_hex = data
        block = Block.parse(io.BytesIO(h2b(block_as_hex)))
        BlockchainUtils.verify(block)
        BlockchainUtils.save(block)
        if TTL < 0:
            forwardMessage = json.dumps({"type":type, "data":data, "ttl":TTL - 1})
            CoinSocket.CoinSocket.forward(forwardMessage, addr, NetNodeDao.searchAddrs())
    elif(ConstantMessage.BROADCASTTRANSACTIONMSG == type):
        TTL = json_receive.get("ttl")
        tc_as_hex = data
        tc = Transaction.parse(io.BytesIO(h2b(tc_as_hex)))
        TransactionUtils.verify(tc)
        TransactionUtils.save(tc)
        if TTL > 0:
            forwardMessage = json.dumps({"type":type, "data":data, "ttl":TTL - 1})
            CoinSocket.CoinSocket.forward(forwardMessage, addr, NetNodeDao.searchAddrs())
    elif(ConstantMessage.REPLYNETNODEMSG == type): 
        lstNetnode = []       
        for netnode_as_hex in data:
            netNode = NetNode.parse(io.BytesIO(h2b(netnode_as_hex)))
            NetNodeDao.save(netNode)
            lstNetnode.append(netNode)
        return lstNetnode  
    elif(ConstantMessage.REPLYBLOCKMSG == type):
        block = Block.parse(io.BytesIO(h2b(data)))
        BlockchainUtils.verify(block)
        BlockchainUtils.save(block)
        return block
    elif(ConstantMessage.REPLYBLOCKIDSMSG == type):
        return data
    else:
        pass        
    return

