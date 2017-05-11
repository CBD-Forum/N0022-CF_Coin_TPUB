'''

@author: Administrator
'''
from pycoin.serialize import b2h_rev

from dao import TransactionDao
from dao.CoinSqlite3 import CoinSqlite3

def __getSearchResult(c):
    return TransactionDao.__getSearchResult(c)

def __getSearchResultSingle(c):
    return TransactionDao.__getSearchResultSingle(c)


# 搜索指定hash的众筹交易
def searchCFTcsByOriginal_hash(original_hash):   
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where original_hash = ? and  parentBlockId != \'\'', original_hash)
    return __getSearchResult(c)

def searchAllCFDict():
    c = CoinSqlite3()._exec_sql('Select * from TransactionInfo where type =2 and target_amount = lack_amount and  parentBlockId != \'\'')
    src_cfs = __getSearchResult(c)
    allCFDict = {}
    for src_cf in src_cfs:
        cfs = searchCFTcsByOriginal_hash(src_cf.hash())
        cfs.insert(0, src_cf)
        allCFDict[src_cf.hash()] = cfs
    return allCFDict
        
    
    