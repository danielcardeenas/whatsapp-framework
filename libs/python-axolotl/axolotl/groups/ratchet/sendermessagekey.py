# -*- coding: utf-8 -*-

from ...kdf.hkdfv3 import HKDFv3
from ...util.byteutil import ByteUtil


class SenderMessageKey:
    def __init__(self, iteration, seed):
        """
        :type iteration: int
        :type seed: bytearray
        """
        derivative = HKDFv3().deriveSecrets(seed, "WhisperGroup".encode(), 48)
        parts = ByteUtil.split(derivative, 16, 32)

        self.iteration = iteration
        self.seed = seed
        self.iv = parts[0]
        self.cipherKey = parts[1]

    def getIteration(self):
        return self.iteration

    def getIv(self):
        return self.iv

    def getCipherKey(self):
        return self.cipherKey

    def getSeed(self):
        return self.seed
