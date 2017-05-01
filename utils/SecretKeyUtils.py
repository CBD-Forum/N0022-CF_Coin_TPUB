'''
Created on 2017年5月1日

@author: Administrator
'''
from model.SecretKey import SecretKey
from dao import SecretKeyDao

def manageKey(secretNum):
    secretKey = SecretKey.create(secretNum);
    SecretKeyDao.save(secretKey)
    print(secretKey)