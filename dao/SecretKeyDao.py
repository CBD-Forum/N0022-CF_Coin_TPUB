'''

@author: Administrator
'''

from dao.CoinSqlite3 import CoinSqlite3
from model.SecretKey import SecretKey

def searchCertByPubAddr(pubkey_addr):
    c = CoinSqlite3()._exec_sql('Select cert from SecretKeyInfo where pubicAddress = ?', pubkey_addr)
    tmp = c.fetchone()
    if tmp == None:
        return ''
    else:
        return '''-----BEGIN CERTIFICATE-----
MIIDLjCCAhagAwIBAgIJAKTZkez5jH1vMA0GCSqGSIb3DQEBBQUAMG8xCzAJBgNV
BAYTAkNOMRAwDgYDVQQIDAdCZWlqaW5nMQ0wCwYDVQQKDARUUFVCMREwDwYDVQQL
DAhTZWN1cml0eTENMAsGA1UEAwwEdHB1YjEdMBsGCSqGSIb3DQEJARYOYWRtaW5A
dHB1Yi5jb20wHhcNMTcwNTA4MDgxMTEwWhcNMjcwNTA2MDgxMTEwWjBvMQswCQYD
VQQGEwJDTjEQMA4GA1UECAwHQmVpamluZzENMAsGA1UECgwEVFBVQjERMA8GA1UE
CwwIU2VjdXJpdHkxDTALBgNVBAMMBHRwdWIxHTAbBgkqhkiG9w0BCQEWDmFkbWlu
QHRwdWIuY29tMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEfStTpZiZKqNHJd2tYj/E
MOGYOxFrh/TTliVA3lXadzablXdB27YqBAQirbGnw+NJuvgxa7CBi/nMqahAMTnC
IGFBC/MLll7T4kS/f359/BiRbs4wMiuWNIzhoRugOAmgo3sweTAJBgNVHRMEAjAA
MCwGCWCGSAGG+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0ZTAd
BgNVHQ4EFgQUZ/QPXuhN9WaAjgAOUhOVNN1cELcwHwYDVR0jBBgwFoAUNUt6r4IA
A3nI7bjzFAXN2SRaapQwDQYJKoZIhvcNAQEFBQADggEBAMlXmy0e8a+KqUKZGW6P
+arugviHapt0QLUAxdFPPwbAQm7/wJYcbguAwPvxUQlHMsdvdSqEdDQeOYiOwft8
IGZ0dzNbynvhyH99tK42p5wgWRQyf4hMHrOnCdCgYUNOUVB0kPsSZ1R1ajSgfE/0
Xsi5Jbhpqpzm2G8NVqnPXeYfzQPZwzSgDs9INLs4Yw6aA8ei1IT8ESPSUtCSbFiT
HDB9G7UT/ZJBG6ZeGGONsf6ZOHZz38OkonBfL/tGS6NQzTFpr4H6yKyA3GlnYLOn
E+FOPdz0PSfhJOsKHY+AXFWPVrKfOimfznDYHpyQ0G6X9s31MAjF1JddRG6Xo1Vl
Ftg=
-----END CERTIFICATE-----
'''

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
