# -*- coding: utf-8 -*-

import codecs
import sys

decode_hex = codecs.getdecoder("hex_codec")


class HexUtil:
    @staticmethod
    def decodeHex(hexString):
        hexString = hexString.encode() if type(hexString) is str else hexString
        result = decode_hex(hexString)[0]
        if sys.version_info >= (3, 0):
            result = result.decode('latin-1')
        return result
