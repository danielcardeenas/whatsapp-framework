# -*- coding: utf-8 -*-

from .ciphertextmessage import CiphertextMessage
from . import whisperprotos_pb2 as whisperprotos
from ..util.byteutil import ByteUtil
from ..legacymessageexception import LegacyMessageException
from ..invalidmessageexception import InvalidMessageException
from ..invalidkeyexception import InvalidKeyException
from ..ecc.curve import Curve
class SenderKeyDistributionMessage(CiphertextMessage):
    def __init__(self, id=None, iteration=None, chainKey=None, signatureKey=None, serialized=None):
        """
        :type id: int
        :type iteration: int
        :type chainKey: bytearray
        :type signatureKey: ECPublicKey
        """


        assert bool(id is not None and iteration is not None and chainKey is not None and signatureKey is not None)\
               ^ bool(serialized),\
            "Either pass arguments or serialized data"

        if serialized:
            try:
                messageParts = ByteUtil.split(serialized, 1, len(serialized)- 1)
                version = messageParts[0][0]
                message = messageParts[1]


                if ByteUtil.highBitsToInt(version) < 3:
                    raise LegacyMessageException("Legacy message: %s" % ByteUtil.highBitsToInt(version))

                if ByteUtil.highBitsToInt(version) > self.__class__.CURRENT_VERSION:
                    raise InvalidMessageException("Unknown version: %s" % ByteUtil.highBitsToInt(version))


                distributionMessage = whisperprotos.SenderKeyDistributionMessage()
                distributionMessage.ParseFromString(message)

                if distributionMessage.id is None or distributionMessage.iteration is None\
                    or distributionMessage.chainKey is None or distributionMessage.signingKey is None:
                    raise InvalidMessageException("Incomplete message")

                self.serialized = serialized

                self.id           = distributionMessage.id
                self.iteration    = distributionMessage.iteration
                self.chainKey     = distributionMessage.chainKey
                self.signatureKey = Curve.decodePoint(bytearray(distributionMessage.signingKey), 0)

            except Exception as e:
                raise InvalidMessageException(e)
        else:
            version = [ByteUtil.intsToByteHighAndLow(self.__class__.CURRENT_VERSION, self.__class__.CURRENT_VERSION)]
            self.id = id
            self.iteration = iteration
            self.chainKey = chainKey
            self.signatureKey = signatureKey
            message = whisperprotos.SenderKeyDistributionMessage()
            message.id = id
            message.iteration = iteration
            message.chainKey= bytes(chainKey)
            message.signingKey = signatureKey.serialize()
            message = message.SerializeToString()
            self.serialized = bytes(ByteUtil.combine(version, message))

    def serialize(self):
        return self.serialized

    def getType(self):
        return self.__class__.SENDERKEY_DISTRIBUTION_TYPE

    def getIteration(self):
        return self.iteration

    def getChainKey(self):
        return self.chainKey

    def getSignatureKey(self):
        return self.signatureKey

    def getId(self):
        return self.id