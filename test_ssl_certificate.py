import OpenSSL
from OpenSSL.crypto import FILETYPE_PEM
cert = open(r'D:\区块链\server-ecc.crt', 'r').read()      
cert_obj = OpenSSL.crypto.load_certificate(FILETYPE_PEM, cert)
cert_obj.get_issuer()#issue 是证书的签发人 CA
cert_obj.get_subject()#subject 是证书的持有人
'''<X509Name object '/C=CN/ST=Beijing/O=TPUB/OU=Security/CN=tpub/emailAddress=admin@tpub.com'>'''
cert_obj.get_issuer().C
''''CN'''

'''/C 国家代码
    /ST 省份/州
    /O 公司，company
    /OU 部门
    /CN 个人名称、代号
    /email 邮箱
    '''
