# -*- coding: utf-8 -*-

from ...state import storageprotos_pb2 as storageprotos
from ..ratchet.senderchainkey import SenderChainKey
from ..ratchet.sendermessagekey import SenderMessageKey
from ...ecc.curve import Curve


class SenderKeyState:
    def __init__(self, id=None, iteration=None, chainKey=None,
                 signatureKeyPublic=None, signatureKeyPrivate=None,
                 signatureKeyPair=None, senderKeyStateStructure=None):
        """
        :type id: int
        :type iteration: int
        :type chainKey:  bytearray
        :type signatureKeyPublic:  ECPublicKey
        :type signatureKeyPrivate: ECPrivateKey
        :type signatureKeyPair: ECKeyPair
        :type senderKeyStateStructure: SenderKeyStateStructure
        """
        assert (bool(id) and bool(iteration) and bool(chainKey)) or \
               (bool(senderKeyStateStructure) ^ bool(signatureKeyPublic or signatureKeyPair)) or \
               (bool(signatureKeyPublic) ^ bool(signatureKeyPair)), "Missing required arguments"

        if senderKeyStateStructure:
            self.senderKeyStateStructure = senderKeyStateStructure
        else:
            if signatureKeyPair:
                signatureKeyPublic = signatureKeyPair.getPublicKey()
                signatureKeyPrivate = signatureKeyPair.getPrivateKey()

            self.senderKeyStateStructure = storageprotos.SenderKeyStateStructure()
            senderChainKeyStructure = self.senderKeyStateStructure.SenderChainKey()
            senderChainKeyStructure.iteration = iteration
            senderChainKeyStructure.seed = chainKey
            self.senderKeyStateStructure.senderChainKey.MergeFrom(senderChainKeyStructure)

            signingKeyStructure = self.senderKeyStateStructure.SenderSigningKey()
            signingKeyStructure.public = signatureKeyPublic.serialize()

            if signatureKeyPrivate:
                signingKeyStructure.private = signatureKeyPrivate.serialize()

            self.senderKeyStateStructure.senderKeyId = id
            self.senderChainKey = senderChainKeyStructure
            self.senderKeyStateStructure.senderSigningKey.CopyFrom(signingKeyStructure)

    def getKeyId(self):
        return self.senderKeyStateStructure.senderKeyId

    def getSenderChainKey(self):
        return SenderChainKey(self.senderKeyStateStructure.senderChainKey.iteration,
                              bytearray(self.senderKeyStateStructure.senderChainKey.seed))

    def setSenderChainKey(self, chainKey):
        self.senderKeyStateStructure.senderChainKey.iteration = chainKey.getIteration()
        self.senderKeyStateStructure.senderChainKey.seed = chainKey.getSeed()

    def getSigningKeyPublic(self):
        return Curve.decodePoint(bytearray(self.senderKeyStateStructure.senderSigningKey.public), 0)

    def getSigningKeyPrivate(self):
        return Curve.decodePrivatePoint(self.senderKeyStateStructure.senderSigningKey.private)

    def hasSenderMessageKey(self, iteration):
        for senderMessageKey in self.senderKeyStateStructure.senderMessageKeys:
            if senderMessageKey.iteration == iteration:
                return True

        return False

    def addSenderMessageKey(self, senderMessageKey):
        smk = self.senderKeyStateStructure.SenderMessageKey()
        smk.iteration = senderMessageKey.iteration
        smk.seed = senderMessageKey.seed
        self.senderKeyStateStructure.senderMessageKeys.extend([smk])

    def removeSenderMessageKey(self, iteration):
        keys = self.senderKeyStateStructure.senderMessageKeys
        result = None

        for i in range(0, len(keys)):
            senderMessageKey = keys[i]
            if senderMessageKey.iteration == iteration:
                result = senderMessageKey
                del keys[i]
                break

        if result is not None:
            return SenderMessageKey(result.iteration, bytearray(result.seed))

        return None

    def getStructure(self):
        return self.senderKeyStateStructure
