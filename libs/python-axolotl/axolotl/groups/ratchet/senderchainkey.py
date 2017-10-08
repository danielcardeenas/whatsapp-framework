# -*- coding: utf-8 -*-

import hashlib
import hmac

from .sendermessagekey import SenderMessageKey


class SenderChainKey:
    MESSAGE_KEY_SEED = bytearray([0x01])
    CHAIN_KEY_SEED = bytearray([0x02])

    def __init__(self, iteration, chainKey):
        """
        :type iteration: int
        :type chainKey: bytearray
        """
        self.iteration = iteration
        self.chainKey = chainKey

    def getIteration(self):
        return self.iteration

    def getSenderMessageKey(self):
        return SenderMessageKey(self.iteration, self.getDerivative(self.__class__.MESSAGE_KEY_SEED, self.chainKey))

    def getNext(self):
        return SenderChainKey(self.iteration + 1, self.getDerivative(self.__class__.CHAIN_KEY_SEED, self.chainKey))

    def getSeed(self):
        return self.chainKey

    def getDerivative(self, seed, key):
        mac = hmac.new(bytes(key), bytes(seed), digestmod=hashlib.sha256)
        return mac.digest()
