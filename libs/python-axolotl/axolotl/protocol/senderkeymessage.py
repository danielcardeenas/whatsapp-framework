# -*- coding: utf-8 -*-

from .ciphertextmessage import CiphertextMessage
from ..util.byteutil import ByteUtil
from ..legacymessageexception import LegacyMessageException
from ..invalidmessageexception import InvalidMessageException
from ..invalidkeyexception import InvalidKeyException
from ..ecc.curve import Curve
from . import whisperprotos_pb2 as whisperprotos


class SenderKeyMessage(CiphertextMessage):
    SIGNATURE_LENGTH = 64

    def __init__(self, keyId=None, iteration=None, ciphertext=None, signatureKey=None, serialized=None):
        assert bool(keyId is not None and iteration is not None and ciphertext is not None and
                    signatureKey is not None) ^ bool(serialized), "Either pass arguments or serialized data"

        if serialized:
            try:
                messageParts = ByteUtil.split(serialized, 1, len(serialized) - 1 - self.__class__.SIGNATURE_LENGTH,
                                              self.__class__.SIGNATURE_LENGTH)

                version = messageParts[0][0]
                message = messageParts[1]
                signature = messageParts[2]

                if ByteUtil.highBitsToInt(version) < 3:
                    raise LegacyMessageException("Legacy message: %s" % ByteUtil.highBitsToInt(version))

                if ByteUtil.highBitsToInt(version) > self.__class__.CURRENT_VERSION:
                    raise InvalidMessageException("Unknown version: %s" % ByteUtil.highBitsToInt(version))

                senderKeyMessage = whisperprotos.SenderKeyMessage()
                senderKeyMessage.ParseFromString(message)

                if senderKeyMessage.id is None or senderKeyMessage.iteration is None or \
                        senderKeyMessage.ciphertext is None:
                    raise InvalidMessageException("Incomplete message")

                self.serialized = serialized
                self.messageVersion = ByteUtil.highBitsToInt(version)

                self.keyId = senderKeyMessage.id
                self.iteration = senderKeyMessage.iteration
                self.ciphertext = senderKeyMessage.ciphertext
            except Exception as e:
                raise InvalidMessageException(e)
        else:
            version = [ByteUtil.intsToByteHighAndLow(self.__class__.CURRENT_VERSION, self.__class__.CURRENT_VERSION)]

            message = whisperprotos.SenderKeyMessage()
            message.id = keyId
            message.iteration = iteration
            message.ciphertext = ciphertext
            message = message.SerializeToString()

            signature = self.getSignature(signatureKey, bytes(ByteUtil.combine(version, message)))

            self.serialized = bytes(ByteUtil.combine(version, message, signature))
            self.messageVersion = self.__class__.CURRENT_VERSION
            self.keyId = keyId
            self.iteration = iteration
            self.ciphertext = ciphertext


    def getKeyId(self):
        return self.keyId

    def getIteration(self):
        return self.iteration

    def getCipherText(self):
        return self.ciphertext

    def verifySignature(self, signatureKey):
        """
        :type signatureKey: ECPublicKey
        """
        try:
            parts = ByteUtil.split(self.serialized,
                                   len(self.serialized) - self.__class__.SIGNATURE_LENGTH,
                                   self.__class__.SIGNATURE_LENGTH)

            if not Curve.verifySignature(signatureKey, parts[0], parts[1]):
                raise InvalidMessageException("Invalid signature!")
        except InvalidKeyException as e:
            raise InvalidMessageException(e)

    def getSignature(self, signatureKey, serialized):
        """
        :type signatureKey: ECPrivateKey
        :type serialized: bytearray
        """
        try:
            return Curve.calculateSignature(signatureKey, serialized)
        except InvalidKeyException as e:
            raise AssertionError(e)

    def serialize(self):
        return self.serialized

    def getType(self):
        return CiphertextMessage.SENDERKEY_TYPE