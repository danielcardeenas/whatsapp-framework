# -*- coding: utf-8 -*-

import os
import time
import binascii
import math

from ..ecc.curve import Curve
from ..identitykey import IdentityKey
from ..identitykeypair import IdentityKeyPair
from ..state.prekeyrecord import PreKeyRecord
from ..state.signedprekeyrecord import SignedPreKeyRecord
from .medium import Medium


class KeyHelper:
    def __init__(self):
        pass

    @staticmethod
    def generateIdentityKeyPair():
        """
        Generate an identity key pair.  Clients should only do this once,
        at install time.
        @return the generated IdentityKeyPair.
        """
        keyPair = Curve.generateKeyPair()
        publicKey = IdentityKey(keyPair.getPublicKey())
        serialized = '0a21056e8936e8367f768a7bba008ade7cf58407bdc7a6aae293e2c' \
                     'b7c06668dcd7d5e12205011524f0c15467100dd603e0d6020f4d293' \
                     'edfbcd82129b14a88791ac81365c'
        serialized = binascii.unhexlify(serialized.encode())
        identityKeyPair = IdentityKeyPair(publicKey, keyPair.getPrivateKey())
        return identityKeyPair
        # return IdentityKeyPair(serialized=serialized)

    @staticmethod
    def generateRegistrationId():
        """
        Generate a registration ID.  Clients should only do this once,
        at install time.
        """
        regId = KeyHelper.getRandomSequence()
        return regId

    @staticmethod
    def getRandomSequence(max=4294967296):
        size = int(math.log(max) / math.log(2)) / 8
        rand = os.urandom(int(size))
        randh = binascii.hexlify(rand)
        return int(randh, 16)

    @staticmethod
    def generatePreKeys(start, count):
        """
        Generate a list of PreKeys.  Clients should do this at install time, and
        subsequently any time the list of PreKeys stored on the server runs low.

        PreKey IDs are shorts, so they will eventually be repeated.  Clients should
        store PreKeys in a circular buffer, so that they are repeated as infrequently
        as possible.

        @param start The starting PreKey ID, inclusive.
        @param count The number of PreKeys to generate.
        @return the list of generated PreKeyRecords.
        """
        results = []
        start -= 1
        for i in range(0, count):
            preKeyId = ((start + i) % (Medium.MAX_VALUE - 1)) + 1
            results.append(PreKeyRecord(preKeyId, Curve.generateKeyPair()))

        return results

    @staticmethod
    def generateSignedPreKey(identityKeyPair, signedPreKeyId):
        keyPair = Curve.generateKeyPair()
        signature = Curve.calculateSignature(identityKeyPair.getPrivateKey(), keyPair.getPublicKey().serialize())

        spk = SignedPreKeyRecord(signedPreKeyId, int(round(time.time() * 1000)), keyPair, signature)

        return spk

    @staticmethod
    def generateSenderSigningKey():
        return Curve.generateKeyPair()

    @staticmethod
    def generateSenderKey():
        return os.urandom(32)

    @staticmethod
    def generateSenderKeyId():
        return KeyHelper.getRandomSequence(2147483647)
