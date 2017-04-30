'''
Created on 2017��4��29��

@author: Administrator
'''
import socket
from socketInfo import ReceiveMessage
from time import sleep


class CoinSocket(object):
    '''
    classdocs
    '''
    
    def __init__(self, srcPort):
        self.port = srcPort
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', self.port))
        print('waiting......')
        while True:
#             ���ղ�����������Ϣ
            data, addr = self.s.recvfrom()
            ReceiveMessage.handleReceiMsg(data, addr)
            sleep(100)
    
    
    def sendMsg(self, json_reply, addr):
        '''ת������ ���͵���ָ��url��������ڵ�'''
        self.s.sendto(json_reply, addr)
    
    def broadcastMsg(self, json_reply, addrs):
        '''ת������ ���͵���ָ��url��������ڵ�'''
        for addr in addrs:
            self.s.sendto(json_reply, addr)
    
    def forward(self, json_reply, addr, addrs):   
        '''ת������ ���͵���ָ��url��������ڵ�'''
        for tmpUrl in addrs:
            if addr != tmpUrl:
                self.s.sendto(json_reply, tmpUrl)
        

  
