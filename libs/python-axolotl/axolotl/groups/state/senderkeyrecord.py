# -*- coding: utf-8 -*-

from ...state.storageprotos_pb2 import SenderKeyRecordStructure
from .senderkeystate import SenderKeyState
from ...invalidkeyidexception import InvalidKeyIdException


class SenderKeyRecord:
    def __init__(self, serialized=None):
        self.senderKeyStates = []

        if serialized:
            senderKeyRecordStructure = SenderKeyRecordStructure()
            senderKeyRecordStructure.ParseFromString(serialized)

            for structure in senderKeyRecordStructure.senderKeyStates:
                self.senderKeyStates.append(SenderKeyState(senderKeyStateStructure=structure))


    def isEmpty(self):
        return len(self.senderKeyStates) == 0

    def getSenderKeyState(self, keyId=None):
        if keyId is None:
            if len(self.senderKeyStates):
                return self.senderKeyStates[0]
            else:
                raise InvalidKeyIdException("No key state in record")
        else:
            for state in self.senderKeyStates:
                if state.getKeyId() == keyId:
                    return state
            raise InvalidKeyIdException("No keys for: %s" % keyId)

    def addSenderKeyState(self, id, iteration, chainKey, signatureKey):
        """
        :type id: int
        :type iteration: int
        :type chainKey: bytearray
        :type signatureKey: ECPublicKey
        """
        self.senderKeyStates.append(SenderKeyState(id, iteration, chainKey, signatureKey))

    def setSenderKeyState(self, id, iteration, chainKey, signatureKey):
        """
        :type id: int
        :type iteration: int
        :type chainKey: bytearray
        :type signatureKey: ECKeyPair
        """
        del self.senderKeyStates[:]
        self.senderKeyStates.append(SenderKeyState(id, iteration, chainKey, signatureKeyPair=signatureKey))

    def serialize(self):
        recordStructure = SenderKeyRecordStructure()

        for senderKeyState in self.senderKeyStates:
            recordStructure.senderKeyStates.extend([senderKeyState.getStructure()])

        return recordStructure.SerializeToString()