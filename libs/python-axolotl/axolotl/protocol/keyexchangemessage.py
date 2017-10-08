# -*- coding: utf-8 -*-

from .ciphertextmessage import CiphertextMessage
from ..util.byteutil import ByteUtil
from . import whisperprotos_pb2 as whisperprotos
from ..legacymessageexception import LegacyMessageException
from ..invalidversionexception import InvalidVersionException
from ..invalidmessageexception import InvalidMessageException
from ..invalidkeyexception import InvalidKeyException
from ..ecc.curve import Curve
from ..identitykey import IdentityKey


class KeyExchangeMessage:
    INITIATE_FLAG = 0x01
    RESPONSE_FLAG = 0X02
    SIMULTAENOUS_INITIATE_FLAG = 0x04

    def __init__(self, messageVersion=None, sequence=None, flags=None, baseKey=None,
                 baseKeySignature=None, ratchetKey=None, identityKey=None, serialized=None):
        """
        :type messageVersion: int
        :type  sequence: int
        :type flags:int
        :type baseKey: ECPublicKey
        :type baseKeySignature: bytearray
        :type ratchetKey: ECPublicKey
        :type identityKey: IdentityKey
        :type serialized: bytearray
        """
        if serialized:
            try:
                parts = ByteUtil.split(serialized, 1, len(serialized) - 1)
                self.version = ByteUtil.highBitsToInt(parts[0][0])
                self.supportedVersion = ByteUtil.lowBitsToInt(parts[0][0])
                if self.version <= CiphertextMessage.UNSUPPORTED_VERSION:
                    raise LegacyMessageException("Unsupportmessageed legacy version: %s" % self.version)
                if self.version > CiphertextMessage.CURRENT_VERSION:
                    raise InvalidVersionException("Unkown version: %s" % self.version)
                message = whisperprotos.KeyExchangeMessage()
                message.ParseFromString(bytes(parts[1]))

                if (not message.HasField("id") or not message.HasField("baseKey") or
                        not message.HasField("ratchetKey") or not message.HasField("identityKey") or
                        (self.version >= 3 and not message.HasField("baseKeySignature"))):
                    raise InvalidMessageException("Some required fields are missing!")

                self.sequence = message.id >> 5
                self.flags = message.id & 0x1f
                self.serialized = serialized
                self.baseKey = Curve.decodePoint(bytearray(message.baseKey), 0)
                self.baseKeySignature = message.baseKeySignature
                self.ratchetKey = Curve.decodePoint(bytearray(message.ratchetKey), 0)
                self.identityKey = IdentityKey(message.identityKey, 0)

            except InvalidKeyException as e:
                raise InvalidMessageException(e)
        else:
            self.supportedVersion = CiphertextMessage.CURRENT_VERSION
            self.version = messageVersion
            self.sequence = sequence
            self.flags = flags
            self.baseKey = baseKey
            self.baseKeySignature = baseKeySignature
            self.ratchetKey = ratchetKey
            self.identityKey = identityKey

            version = [ByteUtil.intsToByteHighAndLow(self.version, self.supportedVersion)]
            keyExchangeMessage = whisperprotos.KeyExchangeMessage()
            keyExchangeMessage.id = (self.sequence << 5) | self.flags
            keyExchangeMessage.baseKey = baseKey.serialize()
            keyExchangeMessage.ratchetKey = ratchetKey.serialize()
            keyExchangeMessage.identityKey = identityKey.serialize()

            if messageVersion >= 3:
                keyExchangeMessage.baseKeySignature = baseKeySignature

            self.serialized = ByteUtil.combine(version, keyExchangeMessage.SerializeToString())

    def getVersion(self):
        return self.version

    def getBaseKey(self):
        return self.baseKey

    def getBaseKeySignature(self):
        return self.baseKeySignature

    def getRatchetKey(self):
        return self.ratchetKey

    def getIdentityKey(self):
        return self.identityKey

    def hasIdentityKey(self):
        return True

    def getMaxVersion(self):
        return self.supportedVersion

    def isResponse(self):
        return ((self.flags & self.__class__.RESPONSE_FLAG) != 0)

    def isInitiate(self):
        return (self.flags & self.__class__.INITIATE_FLAG) != 0

    def isResponseForSimultaneousInitiate(self):
        return (self.flags & self.__class__.SIMULTAENOUS_INITIATE_FLAG) != 0

    def getFlags(self):
        return self.flags

    def getSequence(self):
        return self.sequence

    def serialize(self):
        return self.serialized
