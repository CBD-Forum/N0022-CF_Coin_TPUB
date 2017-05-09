'''
Created on 2017年5月1日

@author: Administrator
'''
import OpenSSL
from OpenSSL.crypto import FILETYPE_PEM

from dao import SecretKeyDao
from model.SecretKey import SecretKey


def manageKey(secretNum):
    secretKey = SecretKey.create(secretNum)
    SecretKeyDao.save(secretKey)
    print(secretKey)
    
def stringToCert(certString):
    return OpenSSL.crypto.load_certificate(FILETYPE_PEM, certString)

def certToString(cert):
    return OpenSSL.crypto.dump_certificate(FILETYPE_PEM, cert).decode()