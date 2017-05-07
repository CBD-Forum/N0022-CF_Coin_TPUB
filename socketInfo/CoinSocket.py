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
     



    
class SendSocket(object):
    @classmethod
    def init(cls):
        port = 9081  
        cls.s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        cls.s.bind(('', port))
        
    @classmethod
    def sendMsg(cls, json_reply, addr):
#         s.sendto(strjson_reply, addr)
        cls.s.sendto(str.encode(json_reply), addr)
    
    @classmethod
    def broadcastMsg(cls, json_reply, addrs):
        print('broadcastMsg......')
        for addr in addrs:
            cls.s.sendto(str.encode(json_reply), addr)
    
    @classmethod
    def forward(cls, json_reply, addr, addrs):   
        for tmpUrl in addrs:
            if addr != tmpUrl:
                cls.s.sendto(str.encode(json_reply), tmpUrl)
        

class ReivSocket(object):     
    def __init__(self):   
        pass     
#         port = 8081  
#         clss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#         s.bind(('', port))
#         t =threading.Thread(target=self.receive,args=())
#         t.start()
#         print('finishing......')
    
    
    @classmethod   
    def init(cls):  
        port = 8081  
        cls.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        cls.s.bind(('', port))
        t =threading.Thread(target=cls.receive,args=())
        t.start()
        print('finishing......')
            
    
    @classmethod    
    def receive(cls):
        print('waiting......')
        while True:
            byte, addr = cls.s.recvfrom(1024)
#             data = bytes.decode(byte)  
            ReceiveMessage.handleReceiMsg(byte, addr)
            sleep(100)    
  
