#!/usr/bin/env python

import argparse
import datetime
import io

from pycoin.networks.default import get_current_netcode
from pycoin.serialize import stream_to_bytes, b2h_rev, b2h, h2b

from dao import BlockchainDao
from dao.CoinSqlite3 import CoinSqlite3
from model.Block import Block
from model.Transaction import dump_tx
from utils import SecretKeyUtils, TransactionUtils
from model.TransactionCF import CFHeader

import time

ZERO32 = b'\0' * 32
def dump_block(block, netcode=None):
    if netcode is None:
        netcode = get_current_netcode()
    blob = stream_to_bytes(block.stream)
    print("%d bytes   block hash %s" % (len(blob), block.id()))
    print("version %d" % block.version)
    print("prior block hash %s" % b2h_rev(block.previous_block_hash))
    print("merkle root %s" % b2h(block.merkle_root))
    print("timestamp %s" % datetime.datetime.utcfromtimestamp(block.timestamp).isoformat())
    print("difficulty %d" % block.difficulty)
    print("nonce %s" % block.nonce)
    print("%d transaction%s" % (len(block.txs), "s" if len(block.txs) != 1 else ""))
    for idx, tx in enumerate(block.txs):
        print("Tx #%d:" % idx)
        dump_tx(tx, netcode=netcode, verbose_signature=1 , disassembly_level=1, do_trace=1, use_pdb=1)


def main():
    parser = argparse.ArgumentParser(description="Dump a block in human-readable form.")
    parser.add_argument("block_bin", nargs="+", type=argparse.FileType('rb'),
                        help='The file containing the binary block.')

    args = parser.parse_args()
    pbkey = '1693NYwCPZYAdF1pYdVfrfCR6c9acpNGQd'
    cf_header = CFHeader(ZERO32, 10, pbkey, time.time()+3600, ZERO32, 10)
    TransactionUtils.createCFTransaction([], cf_header, spendValue=0, publicAddrToValueDict={})
#     TransactionUtils.createFirstTransaction({"17ZaizPFAB76bVXXDZNMHunzeoFjrwGtS2":100})
#     for f in args.block_bin:
#         block = Block.parse(f) 
#          
#         BlockchainDao.save(block)
#         print(block.hash())
#         tmp = BlockchainDao.search(block.hash())
#         print(tmp.hash())
#         dump_block(block)
#         print('')
#         
#         for i in range(1,30):
#             SecretKeyUtils.manageKey(10*i)

if __name__ == '__main__':
    main()
