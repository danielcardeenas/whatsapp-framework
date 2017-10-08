# -*- coding: utf-8 -*-

from ...groups.state.senderkeystore import SenderKeyStore
from ...groups.state.senderkeyrecord import SenderKeyRecord


class InMemorySenderKeyStore(SenderKeyStore):
    def __init__(self):
        self.store = {}

    def storeSenderKey(self, senderKeyName, senderKeyRecord):
        self.store[senderKeyName] = senderKeyRecord

    def loadSenderKey(self, senderKeyName):
        if senderKeyName in self.store:
            return SenderKeyRecord(serialized=self.store[senderKeyName].serialize())

        return SenderKeyRecord()
