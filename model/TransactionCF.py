# -*- coding: utf-8 -*-
"""
Parse, stream, create, sign and verify Bitcoin transactions as Tx structures.


The MIT License (MIT)

Copyright (c) 2013 by Richard Kiss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import io
import warnings

from pycoin.convention import SATOSHI_PER_COIN
from pycoin.serialize.bitcoin_streamer import parse_struct, parse_bc_int, \
    parse_bc_string
from pycoin.tx import Spendable
from model.Transaction import Transaction
from model.TransactionIn import TransactionIn
from model.TransactionOut import TransactionOut


MAX_MONEY = 21000000 * SATOSHI_PER_COIN
MAX_BLOCK_SIZE = 1000000

SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
SIGHASH_ANYONECANPAY = 0x80

ZERO32 = b'\0' * 32

class CFHeader():
    def __init__(self, original_hash, target_amount, pubkey, end_time, pre_hash, lack_amount):
        self.original_hash=original_hash        #起始块hash
        self.target_amount=target_amount    #目标数量
        self.pubkey=pubkey  #众筹人公钥地址
        self.end_time=end_time  #截至时间
        self.pre_hash=pre_hash  #前一块的hash
        self.lack_amount=lack_amount    #剩余筹钱数量

class TransactionCF(Transaction):
    TxIn = TransactionIn
    TxOut = TransactionOut
    Spendable = Spendable

    MAX_MONEY = MAX_MONEY
    MAX_TX_SIZE = MAX_BLOCK_SIZE

    SIGHASH_ALL = SIGHASH_ALL
    SIGHASH_NONE = SIGHASH_NONE
    SIGHASH_SINGLE = SIGHASH_SINGLE
    SIGHASH_ANYONECANPAY = SIGHASH_ANYONECANPAY

    ALLOW_SEGWIT = True

    @classmethod
    def parse(class_, f, allow_segwit=None):
        """Parse a Bitcoin transaction Tx from the file-like object f."""
        if allow_segwit is None:
            allow_segwit = class_.ALLOW_SEGWIT
        txs_in = []
        txs_out = []
        original_hash, target_amount, pubkey, end_time, pre_hash, lack_amount = parse_struct("#QSL#Q", f)
            
        version, = parse_struct("L", f)
        v1 = ord(f.read(1))
        is_segwit = allow_segwit and (v1 == 0)
        v2 = None
        if is_segwit:
            flag = f.read(1)
            if flag == b'\0':
                raise ValueError("bad flag in segwit")
            if flag == b'\1':
                v1 = None
            else:
                is_segwit = False
                v2 = ord(flag)
        count = parse_bc_int(f, v=v1)
        txs_in = []
        for i in range(count):
            txs_in.append(class_.TxIn.parse(f))
        count = parse_bc_int(f, v=v2)
        txs_out = []
        for i in range(count):
            txs_out.append(class_.TxOut.parse(f))

        if is_segwit:
            for tx_in in txs_in:
                stack = []
                count = parse_bc_int(f)
                for i in range(count):
                    stack.append(parse_bc_string(f))
                tx_in.witness = stack
        lock_time, = parse_struct("L", f)
        return class_(CFHeader(original_hash, target_amount, pubkey, end_time, pre_hash, lack_amount), version, txs_in, txs_out, lock_time)



    def __init__(self, cf_header, version, txs_in, txs_out, lock_time=0, unspents=None, state = 0, uid = 0):
        super().__init__(version, txs_in, txs_out, lock_time, unspents, state, uid)
        self.cf_header = cf_header
#         self.tx_type = 0x02
        

 
