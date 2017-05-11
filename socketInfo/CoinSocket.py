'''

@author: Administrator
'''



from _thread import start_new_thread
import asyncio
import socket
from test.libregrtest.main import printlist
import threading
from time import sleep
import traceback
from urllib.parse import urlencode

import Constants
from socketInfo import ReceiveMessage


class SendSocket(object):
    @classmethod
    def init(cls): 
        try:
            port = Constants.SEND_PORT  
            cls.s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            cls.s.bind(('', port))
        except:  
            traceback.print_exc() 
        
    @classmethod
    def sendMsg(cls, json_reply, addr): 
        try:
    #         s.sendto(strjson_reply, addr)
            cls.s.sendto(str.encode(json_reply), addr)
        except:  
            traceback.print_exc() 
    
    @classmethod
    def broadcastMsg(cls, json_reply, addrs): 
        try:
            print('broadcastMsg......')
            printlist(addrs)
            for addr in addrs:
                cls.s.sendto(str.encode(json_reply), addr)
        except:  
            traceback.print_exc() 
    
    @classmethod
    def forward(cls, json_reply, addr, addrs):   
        try:
            for tmpUrl in addrs:
                if addr != tmpUrl:
                    cls.s.sendto(str.encode(json_reply), tmpUrl)
        except:  
            traceback.print_exc() 
        

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
        try:
            port = Constants.RECEIVE_PORT  
            cls.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            cls.s.bind(('', port))
            t =threading.Thread(target=cls.receive,args=())
            t.start()
            print('finishing init Receiv......')
        except:  
            traceback.print_exc()  
            
    
    @classmethod    
    def receive(cls):
        try:
            print('waiting messages......')
            while True:
                byte, addr = cls.s.recvfrom(102400)
    #             data = bytes.decode(byte)  
                ReceiveMessage.handleReceiMsg(byte, addr)
                sleep(100)  
        except:  
            traceback.print_exc()   
  
