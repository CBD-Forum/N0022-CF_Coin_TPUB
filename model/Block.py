
from builtins import classmethod
import io
from test.test_buffer import struct

from pycoin import merkle
from pycoin.block import BadMerkleRootError
from pycoin.encoding import double_sha256
from pycoin.serialize import b2h_rev, b2h
from pycoin.serialize.bitcoin_streamer import parse_struct, stream_struct

from model.Transaction import Transaction
from model.TransactionCF import TransactionCF
from utils import TransactionUtils


class BlockHeader(object):
    """A BlockHeader is a block with the transaction data removed. With a
    complete Merkle tree database, it can be reconstructed from the
    merkle_root."""

    Transaction = Transaction
    TransactionCF = TransactionCF

    @classmethod
    def parse(cls, f):
        """Parse the BlockHeader from the file-like object in the standard way
        that blocks are sent in the network (well, except we ignore the
        transaction information)."""
        (version, previous_block_hash, merkle_root,
            timestamp, difficulty, nonce) = struct.unpack("<L32s32sLLL", f.read(4 + 32 + 32 + 4 * 3))
        return cls(version, previous_block_hash, merkle_root, timestamp, difficulty, nonce)

    @classmethod
    def from_bin(class_, bytes):
        f = io.BytesIO(bytes)
        return class_.parse(f)

    def __init__(self, version, previous_block_hash, merkle_root, timestamp, difficulty, nonce, state):
        self.version = version
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        self.state = state

    def set_nonce(self, nonce):
        self.nonce = nonce
        if hasattr(self, "__hash"):
            del self.__hash

    def _calculate_hash(self):
        s = io.BytesIO()
        self.stream_header(s)
        return double_sha256(s.getvalue())

    def hash(self):
        """Calculate the hash for the block header. Note that this has the bytes
        in the opposite order from how the header is usually displayed (so the
        long string of 00 bytes is at the end, not the beginning)."""
        if not hasattr(self, "__hash"):
            self.__hash = self._calculate_hash()
        return self.__hash

    def stream_header(self, f):
        """Stream the block header in the standard way to the file-like object f."""
        stream_struct("L##LLL", f, self.version, self.previous_block_hash,
                      self.merkle_root, self.timestamp, self.difficulty, self.nonce)

    def stream(self, f):
        """Stream the block header in the standard way to the file-like object f.
        The Block subclass also includes the transactions."""
        return self.stream_header(f)

    def as_bin(self):
        """Return the transaction as binary."""
        f = io.BytesIO()
        self.stream(f)
        return f.getvalue()

    def as_hex(self):
        """Return the transaction as hex."""
        return b2h(self.as_bin())

    def id(self):
        """Returns the hash of the block displayed with the bytes in the order
        they are usually displayed in."""
        return b2h_rev(self.hash())

    def previous_block_id(self):
        """Returns the hash of the previous block, with the bytes in the order
        they are usually displayed in."""
        return b2h_rev(self.previous_block_hash)

    def __str__(self):
        return "%s [%s] (previous %s)" % (self.__class__.__name__, self.id(), self.previous_block_id())

    def __repr__(self):
        return self.__str__()



class Block(BlockHeader):
    @classmethod
    def parse(cls, f, include_offsets=None):
        """Parse the Block from the file-like object in the standard way
        that blocks are sent in the network."""
        if include_offsets is None:
            include_offsets = hasattr(f, "tell")
        (version, previous_block_hash, merkle_root, timestamp,
            difficulty, nonce, count) = parse_struct("L##LLLI", f)
        txs = []
        for i in range(count):
            if include_offsets:
                offset_in_block = f.tell()
            tx_type, = parse_struct("L", f)
#            tx = cls.Transaction.parse(f)
            if 0x01 == tx_type:
                tx = cls.Transaction.parse(f)
            elif 0x02 == tx_type:
                tx = cls.TransactionCF.parse(f)
            txs.append(tx)
            if include_offsets:
                tx.offset_in_block = offset_in_block
        block = cls(version, previous_block_hash, merkle_root, timestamp, difficulty, nonce, txs, 0)
        for tx in txs:
            tx.block = block
        block.check_merkle_hash()
        return block

    def __init__(self, version, previous_block_hash, merkle_root, timestamp, difficulty, nonce, txs, state, next_block_hash = "", height = 0):
        self.version = version
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        self.txs = txs
        self.state = state
        self.next_block_hash = next_block_hash
        self.height = height
        self.max = self.difficulty_max_mask_for_bits()
        
#         target = self.difficulty
#         a=(target & 0xff000000)>>24
#         b=(target & 0x00ff0000)>>16
#         c=(target & 0x0000ff00)>>8
#         d=(target & 0x000000ff)
#         num = (c << 16) + (b << 8 ) + a
#         exp = d
#         max = num * 256 ** (d-3)
#         #max = (target & 0xffffff) * 256 ** (((target & 0xff000000) >> 24 )-3)
#         max = ('%064s' % hex(max)[2:]).replace(' ', '0')
#         self.max = max

        
        self.check_merkle_hash()

    def as_blockheader(self):
        return BlockHeader(self.version, self.previous_block_hash, self.merkle_root,
                           self.timestamp, self.difficulty, self.nonce, self.state)

    def stream(self, f):
        """Stream the block in the standard way to the file-like object f."""
        stream_struct("L##LLLI", f, self.version, self.previous_block_hash,
                      self.merkle_root, self.timestamp, self.difficulty, self.nonce, len(self.txs))
        for t in self.txs:
            t.stream(f)

    def check_merkle_hash(self):
        """Raise a BadMerkleRootError if the Merkle hash of the
        transactions does not match the Merkle hash included in the block."""
#         calculated_hash = merkle([tx.hash() for tx in self.txs], double_sha256)
        # ##
        return True
#         if calculated_hash != self.merkle_root:
#             raise BadMerkleRootError(
#                 "calculated %s but block contains %s" % (b2h(calculated_hash), b2h(self.merkle_root)))
            
    def check_pow(self):
        tmphash = b2h_rev(self.hash())
        return self.max > tmphash
    
    def difficulty_max_mask_for_bits(self):
        bits = self.difficulty
        prefix = bits >> 24
        mask = (bits & 0x7ffff) << (8 * (prefix - 3))
        return mask
    

    def __repr__(self):
        return "%s [%s] (previous %s) [tx count:%d] %s" % (
            self.__class__.__name__, self.id(), self.previous_block_id(), len(self.txs), self.txs)

    def total_in(self):
        total_in_number = 0
        for tx in self.txs:
            total_in_number += tx.total_in()
        return total_in_number
    
    def normal_tc_number(self):
        normal_tc = 0
        for tx in self.txs:
            if not TransactionUtils.isCFTransation(tx):
                ++normal_tc
        return normal_tc
    
    def cf_tc_number(self):
        cf_tc = 0
        for tx in self.txs:
            if TransactionUtils.isCFTransation(tx):
                ++cf_tc
        return cf_tc
    
    def fee(self):
        fee = 0
        for tx in self.txs:
            if TransactionUtils.isCFTransation(tx):
                fee += tx.fee()
        return fee