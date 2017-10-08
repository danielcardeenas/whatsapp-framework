# -*- coding: utf-8 -*-

import abc
import hmac
import hashlib
import math


class HKDF(object):
    __metaclass__ = abc.ABCMeta
    HASH_OUTPUT_SIZE = 32

    @staticmethod
    def createFor(messageVersion):
        from .hkdfv2 import HKDFv2
        from .hkdfv3 import HKDFv3

        if messageVersion == 2:
            return HKDFv2()
        elif messageVersion == 3:
            return HKDFv3()
        else:
            raise AssertionError("Unknown version: %s " % messageVersion)

    def deriveSecrets(self, inputKeyMaterial, info, outputLength, salt=None):
        salt = salt or bytearray(self.__class__.HASH_OUTPUT_SIZE)
        prk = self.extract(salt, inputKeyMaterial)
        return self.expand(prk, info, outputLength)

    def extract(self, salt, inputKeyMaterial):
        mac = hmac.new(bytes(salt), digestmod=hashlib.sha256)
        mac.update(bytes(inputKeyMaterial))
        return mac.digest()

    def expand(self, prk, info, outputSize):
        iterations = int(math.ceil(float(outputSize) / float(self.__class__.HASH_OUTPUT_SIZE)))
        mixin = bytearray()
        results = bytearray()
        remainingBytes = outputSize

        for i in range(self.getIterationStartOffset(), iterations + self.getIterationStartOffset()):
            mac = hmac.new(prk, digestmod=hashlib.sha256)
            mac.update(bytes(mixin))
            if info is not None:
                mac.update(bytes(info))
            updateChr = chr(i % 256)
            mac.update(updateChr.encode())

            stepResult = mac.digest()
            stepSize = min(remainingBytes, len(stepResult))
            results.extend(stepResult[:stepSize])
            mixin = stepResult
            remainingBytes -= stepSize

        return bytes(results)

    @abc.abstractmethod
    def getIterationStartOffset(self):
        return 0
