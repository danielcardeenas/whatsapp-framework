# -*- coding: utf-8 -*-
from ..protocol.senderkeydistributionmessage import SenderKeyDistributionMessage
from ..invalidkeyidexception import InvalidKeyIdException
from ..invalidkeyexception import InvalidKeyException
from ..util.keyhelper import KeyHelper
class GroupSessionBuilder:
    def __init__(self, senderKeyStore):
        self.senderKeyStore = senderKeyStore

    def process(self, senderKeyName, senderKeyDistributionMessage):
        """
        :type senderKeyName: SenderKeyName
        :type senderKeyDistributionMessage: SenderKeyDistributionMessage
        """
        senderKeyRecord = self.senderKeyStore.loadSenderKey(senderKeyName)
        senderKeyRecord.addSenderKeyState(senderKeyDistributionMessage.getId(),
                                          senderKeyDistributionMessage.getIteration(),
                                          senderKeyDistributionMessage.getChainKey(),
                                          senderKeyDistributionMessage.getSignatureKey())
        self.senderKeyStore.storeSenderKey(senderKeyName, senderKeyRecord)


    def create(self, senderKeyName):
        """
        :type senderKeyName: SenderKeyName
        """
        try:
            senderKeyRecord = self.senderKeyStore.loadSenderKey(senderKeyName);

            if senderKeyRecord.isEmpty() :
                senderKeyRecord.setSenderKeyState(KeyHelper.generateSenderKeyId(),
                                                0,
                                                KeyHelper.generateSenderKey(),
                                                KeyHelper.generateSenderSigningKey());
                self.senderKeyStore.storeSenderKey(senderKeyName, senderKeyRecord);

            state = senderKeyRecord.getSenderKeyState();

            return SenderKeyDistributionMessage(state.getKeyId(),
                                                state.getSenderChainKey().getIteration(),
                                                state.getSenderChainKey().getSeed(),
                                                state.getSigningKeyPublic());
        except (InvalidKeyException, InvalidKeyIdException) as e:
            raise AssertionError(e)
