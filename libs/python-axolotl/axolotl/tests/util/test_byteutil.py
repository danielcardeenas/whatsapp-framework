# -*- coding: utf-8 -*-

import unittest

from ...util.byteutil import ByteUtil
# from ...util.hexutil import HexUtil


class ByteUtilTest(unittest.TestCase):
    def test_split(self):
        # okm = HexUtil.decodeHex('02a9aa6c7dbd64f9d3aa92f92a277bf54609dadf0b00'
        #                         '828acfc61e3c724b84a7bfbe5efb603030526742e3ee'
        #                         '89c7024e884e440f1ff376bb2317b2d64deb7c8322f4'
        #                         'c5015d9d895849411ba1d793a827')

        data = [i for i in range(0, 80)]
        a_data = [i for i in range(0, 32)]
        b_data = [i for i in range(32, 64)]
        c_data = [i for i in range(64, 80)]

        a, b, c = ByteUtil.split(data, 32, 32, 16)

        self.assertEqual(a, a_data)
        self.assertEqual(b, b_data)
        self.assertEqual(c, c_data)
