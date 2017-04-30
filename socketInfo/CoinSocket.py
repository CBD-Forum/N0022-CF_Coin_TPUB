'''

@author: Administrator
'''
import socket
from socketInfo import ReceiveMessage
from time import sleep
from _thread import start_new_thread
from urllib.parse import urlencode
import asyncio
import threading

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class CoinSocket(object):
    def receive(self):
        print('waiting......')
        while True:
            byte, addr = s.recvfrom(1024)
            data = bytes.decode(byte)  
            ReceiveMessage.handleReceiMsg(data, addr)
            sleep(100)
        
    def __init__(self, srcPort):
        self.port = srcPort
#         self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('',self.port))
        t =threading.Thread(target=self.receive,args=())
        t.start()
        print('going......')
    
    @classmethod
    def sendMsg(cls, json_reply, addr):
#         s.sendto(strjson_reply, addr)
        s.sendto(str.encode(json_reply), addr)
    
    @classmethod
    def broadcastMsg(cls, json_reply, addrs):
        print('broadcastMsg......')
        for addr in addrs:
            s.sendto(str.encode(json_reply), addr)
    
    @classmethod
    def forward(cls, json_reply, addr, addrs):   
        for tmpUrl in addrs:
            if addr != tmpUrl:
                s.sendto(str.encode(json_reply), tmpUrl)
        

  
