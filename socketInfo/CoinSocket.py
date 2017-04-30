'''
Created on 2017年4月29日

@author: Administrator
'''
import socket
from socketInfo import ReceiveMessage
from time import sleep


class CoinSocket(object):
    '''
    classdocs
    '''
    
    def __init__(self, srcIp, srcPort):
        self.ip = srcIp
        self.port = srcPort
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', self.port))
        print('waiting......')
        while True:
#             接收并处理请求消息
            data, addr = self.s.recvfrom()
            ReceiveMessage.handleReceiMsg(data, addr)
            sleep(100)
    
    
    def sendMsg(self, json_reply, addr):
        '''转发区块 发送到除指定url外的其他节点'''
        self.s.sendto(json_reply, addr)
    
    def broadcastMsg(self, json_reply, addrs):
        '''转发区块 发送到除指定url外的其他节点'''
        for addr in addrs:
            self.s.sendto(json_reply, addr)
    
    def forward(self, json_reply, addr, addrs):   
        '''转发区块 发送到除指定url外的其他节点'''
        for tmpUrl in addrs:
            if addr != tmpUrl:
                self.s.sendto(json_reply, tmpUrl)
        

  
