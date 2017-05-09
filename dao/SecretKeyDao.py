'''

@author: Administrator
'''

from dao.CoinSqlite3 import CoinSqlite3
from model.SecretKey import SecretKey


def search():   
    c = CoinSqlite3()._exec_sql('Select * from SecretKeyInfo')
    secrets = []
    for tmp in c.fetchall():
        secret = SecretKey(tmp[1], tmp[3], tmp[2], tmp[4], tmp[0])
        secrets.append(secret)
    return secrets

def isMypubicAddress(pubicAddress):
    c = CoinSqlite3()._exec_sql('Select * from SecretKeyInfo Where privateKey != \'\' And pubicAddress = ?', pubicAddress)
    tmp = c.fetchone()
    return 0 if tmp == None else 1

def searchMySecrets():   
    c = CoinSqlite3()._exec_sql('Select * from SecretKeyInfo Where privateKey != \'\'')
    secrets = []
    for tmp in c.fetchall():
        secret = SecretKey(tmp[1], tmp[3], tmp[2], tmp[4], tmp[0])
        secrets.append(secret)
    return secrets

def save(secret):
    if isExist(secret):
        update(secret)
    else:
        insert(secret)


def insert(secret):
    CoinSqlite3().exec_sql('INSERT INTO SecretKeyInfo(publicKey, privateKey,pubicAddress, cert) VALUES (?,?,?,?)', str(secret.publicKey), str(secret.privateKey), str(secret.pubicAddress), str(secret.cert)) 
              
def update(secret):
    pass
                
def isExist(secret):
    tmp = CoinSqlite3()._exec_sql('Select * from SecretKeyInfo where publicKey = ?', str(secret.publicKey))
    s = tmp.fetchone()
    return s != None
