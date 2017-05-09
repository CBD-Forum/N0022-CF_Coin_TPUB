'''
Created on 2017年5月1日

@author: Administrator
'''
from pycoin.key import Key


class SecretKey(object):
    '''
    classdocs
    '''

    def __init__(self, publicKey, pubicAddress, privateKey='', cert = '', uid = 0):
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.pubicAddress = pubicAddress
        self.cert = cert
        self.uid = uid
#         if '' != privateKey:            
#             self.key_obj = Key(public_pair=[publicKey, privateKey])
#             self.pubicAddress = self.key_obj.address()
    
    @classmethod    
    def create(cls, sec_num):
        key_obj = Key(secret_exponent=sec_num)
        publicKey, privateKey = key_obj._public_pair
        key_obj = Key(public_pair=[publicKey, privateKey])
        pubicAddress = key_obj.address()
        
        cert = '''-----BEGIN CERTIFICATE-----
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
        return cls(publicKey, pubicAddress, privateKey, cert)
#         self.pubicAddress = key_obj.address()
#         self.key_obj = key_obj
