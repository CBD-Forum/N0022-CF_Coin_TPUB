'''
Created on 2017年5月1日

@author: Administrator
'''
from dao import SecretKeyDao, TransactionOutDao
from model.TransactionOut import TransactionOut

def receiveMoney(tx_id):
    secretKeys = SecretKeyDao.searchMySecrets()
    myPublicAddr = []
    for secret in secretKeys:
        myPublicAddr.append(secret.pubicAddress)
    
    tx_outs = TransactionOutDao.searchAll()
    tx_myins = [];
    for tx_out in tx_outs:
        if tx_out.address() in myPublicAddr:
            tx_myins.append(tx_out)
    

def main():
   pass
   
if __name__ == '__main__':
    main()
