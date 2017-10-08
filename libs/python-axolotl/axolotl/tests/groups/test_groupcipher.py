# -*- coding: utf-8 -*-

import unittest

from .inmemorysenderkeystore import InMemorySenderKeyStore
from ...groups.groupsessionbuilder import GroupSessionBuilder
from ...util.keyhelper import KeyHelper
from ...groups.groupcipher import GroupCipher
from ...duplicatemessagexception import DuplicateMessageException
from ...nosessionexception import NoSessionException
from ...groups.senderkeyname import SenderKeyName
from ...axolotladdress import AxolotlAddress
from ...protocol.senderkeydistributionmessage import SenderKeyDistributionMessage

SENDER_ADDRESS = AxolotlAddress("+14150001111", 1)
GROUP_SENDER   = SenderKeyName("nihilist history reading group", SENDER_ADDRESS);



class GroupCipherTest(unittest.TestCase):

    def test_noSession(self):
        aliceStore = InMemorySenderKeyStore();
        bobStore = InMemorySenderKeyStore();

        aliceSessionBuilder = GroupSessionBuilder(aliceStore)
        bobSessionBuilder   = GroupSessionBuilder(bobStore)

        aliceGroupCipher = GroupCipher(aliceStore, GROUP_SENDER)
        bobGroupCipher = GroupCipher(bobStore, GROUP_SENDER);

        sentAliceDistributionMessage = aliceSessionBuilder.create(GROUP_SENDER);
        receivedAliceDistributionMessage = SenderKeyDistributionMessage(serialized = sentAliceDistributionMessage.serialize());

        ciphertextFromAlice = aliceGroupCipher.encrypt("smert ze smert");

        try:
            plaintextFromAlice = bobGroupCipher.decrypt(ciphertextFromAlice);
            raise AssertionError("Should be no session!");
        except NoSessionException as e:
            pass
    def test_basicEncryptDecrypt(self):
        aliceStore = InMemorySenderKeyStore();
        bobStore = InMemorySenderKeyStore();

        aliceSessionBuilder = GroupSessionBuilder(aliceStore)
        bobSessionBuilder = GroupSessionBuilder(bobStore)

        aliceGroupCipher = GroupCipher(aliceStore, GROUP_SENDER)
        bobGroupCipher = GroupCipher(bobStore, GROUP_SENDER);

        sentAliceDistributionMessage = aliceSessionBuilder.create(GROUP_SENDER);
        receivedAliceDistributionMessage = SenderKeyDistributionMessage(serialized = sentAliceDistributionMessage.serialize());

        bobSessionBuilder.process(GROUP_SENDER, receivedAliceDistributionMessage)

        ciphertextFromAlice = aliceGroupCipher.encrypt("smert ze smert")
        plaintextFromAlice = bobGroupCipher.decrypt(ciphertextFromAlice)

        self.assertEqual(plaintextFromAlice, "smert ze smert")

    def test_basicRatchet(self):
        aliceStore = InMemorySenderKeyStore()
        bobStore = InMemorySenderKeyStore()

        aliceSessionBuilder = GroupSessionBuilder(aliceStore)
        bobSessionBuilder = GroupSessionBuilder(bobStore)

        aliceGroupCipher = GroupCipher(aliceStore, "groupWithBobInIt")
        bobGroupCipher   = GroupCipher(bobStore, "groupWithBobInIt::aliceUserName")

        aliceGroupCipher = GroupCipher(aliceStore, GROUP_SENDER)
        bobGroupCipher   = GroupCipher(bobStore, GROUP_SENDER);

        sentAliceDistributionMessage = aliceSessionBuilder.create(GROUP_SENDER);
        receivedAliceDistributionMessage = SenderKeyDistributionMessage(serialized = sentAliceDistributionMessage.serialize());

        bobSessionBuilder.process(GROUP_SENDER, receivedAliceDistributionMessage)

        ciphertextFromAlice  = aliceGroupCipher.encrypt("smert ze smert")
        ciphertextFromAlice2 = aliceGroupCipher.encrypt("smert ze smert2")
        ciphertextFromAlice3 = aliceGroupCipher.encrypt("smert ze smert3")

        plaintextFromAlice = bobGroupCipher.decrypt(ciphertextFromAlice)

        try:
            bobGroupCipher.decrypt(ciphertextFromAlice)
            raise AssertionError("Should have ratcheted forward!")
        except DuplicateMessageException as dme:
            # good
            pass

        plaintextFromAlice2 = bobGroupCipher.decrypt(ciphertextFromAlice2)
        plaintextFromAlice3 = bobGroupCipher.decrypt(ciphertextFromAlice3)

        self.assertEqual(plaintextFromAlice,"smert ze smert")
        self.assertEqual(plaintextFromAlice2, "smert ze smert2")
        self.assertEqual(plaintextFromAlice3, "smert ze smert3")


    def test_outOfOrder(self):
        aliceStore = InMemorySenderKeyStore();
        bobStore   = InMemorySenderKeyStore();

        aliceSessionBuilder = GroupSessionBuilder(aliceStore)
        bobSessionBuilder   = GroupSessionBuilder(bobStore)

        aliceGroupCipher = GroupCipher(aliceStore, "groupWithBobInIt")
        bobGroupCipher   = GroupCipher(bobStore, "groupWithBobInIt::aliceUserName")

        aliceGroupCipher = GroupCipher(aliceStore, GROUP_SENDER)
        bobGroupCipher = GroupCipher(bobStore, GROUP_SENDER);

        sentAliceDistributionMessage = aliceSessionBuilder.create(GROUP_SENDER);
        receivedAliceDistributionMessage = SenderKeyDistributionMessage(serialized = sentAliceDistributionMessage.serialize());

        bobSessionBuilder.process(GROUP_SENDER, receivedAliceDistributionMessage)

        ciphertexts = []
        for i in range(0, 100):
            ciphertexts.append(aliceGroupCipher.encrypt("up the punks"))
        while len(ciphertexts) > 0:
            index = KeyHelper.getRandomSequence(2147483647) % len(ciphertexts)
            ciphertext = ciphertexts.pop(index)
            plaintext = bobGroupCipher.decrypt(ciphertext)
            self.assertEqual(plaintext, "up the punks")

    def test_encryptNoSession(self):

        aliceStore = InMemorySenderKeyStore()
        aliceGroupCipher = GroupCipher(aliceStore, "groupWithBobInIt")
        try:
            aliceGroupCipher.encrypt("up the punks")
            raise AssertionError("Should have failed!")
        except NoSessionException as nse:
            # good
            pass