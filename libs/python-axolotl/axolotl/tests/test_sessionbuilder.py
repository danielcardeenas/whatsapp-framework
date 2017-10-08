# -*- coding: utf-8 -*-

import unittest
import time
import sys

from ..sessionbuilder import SessionBuilder
from ..sessioncipher import SessionCipher
from ..ecc.curve import Curve
from ..protocol.ciphertextmessage import CiphertextMessage
from ..protocol.whispermessage import WhisperMessage
from ..protocol.prekeywhispermessage import PreKeyWhisperMessage
from ..state.prekeybundle import PreKeyBundle
from ..tests.inmemoryaxolotlstore import InMemoryAxolotlStore
from ..state.prekeyrecord import PreKeyRecord
from ..state.signedprekeyrecord import SignedPreKeyRecord
from ..tests.inmemoryidentitykeystore import InMemoryIdentityKeyStore
from ..protocol.keyexchangemessage import KeyExchangeMessage
from ..untrustedidentityexception import UntrustedIdentityException


class SessionBuilderTest(unittest.TestCase):
    ALICE_RECIPIENT_ID = 5
    BOB_RECIPIENT_ID = 2

    def test_basicPreKeyV2(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             self.__class__.BOB_RECIPIENT_ID,
                                             1)

        bobStore = InMemoryAxolotlStore()
        bobPreKeyPair = Curve.generateKeyPair()
        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1, 31337, bobPreKeyPair.getPublicKey(),
                                 0, None, None, bobStore.getIdentityKeyPair().getPublicKey())

        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

        self.assertTrue(aliceStore.containsSession(self.__class__.BOB_RECIPIENT_ID, 1))
        self.assertEqual(aliceStore.loadSession(self.__class__.BOB_RECIPIENT_ID,
                                                1).getSessionState().getSessionVersion(), 2)

        originalMessage = "L'homme est condamné à être libre"
        aliceSessionCipher = SessionCipher(aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           self.__class__.BOB_RECIPIENT_ID,
                                           1)
        outgoingMessage = aliceSessionCipher.encrypt(originalMessage)

        self.assertTrue(outgoingMessage.getType() == CiphertextMessage.PREKEY_TYPE)

        incomingMessage = PreKeyWhisperMessage(serialized=outgoingMessage.serialize())
        bobStore.storePreKey(31337, PreKeyRecord(bobPreKey.getPreKeyId(), bobPreKeyPair))

        bobSessionCipher = SessionCipher(bobStore, bobStore, bobStore, bobStore, self.__class__.ALICE_RECIPIENT_ID, 1)
        plaintext = bobSessionCipher.decryptPkmsg(incomingMessage)
        if sys.version_info >= (3,0): plaintext = plaintext.decode()

        self.assertTrue(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))
        self.assertTrue(bobStore.loadSession(self.__class__.ALICE_RECIPIENT_ID,
                        1).getSessionState().getSessionVersion() == 2)
        self.assertEqual(originalMessage, plaintext)

        bobOutgoingMessage = bobSessionCipher.encrypt(originalMessage)
        self.assertTrue(bobOutgoingMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        alicePlaintext = aliceSessionCipher.decryptMsg(bobOutgoingMessage)
        if sys.version_info >= (3,0): alicePlaintext = alicePlaintext.decode()
        self.assertEqual(alicePlaintext, originalMessage)

        self.runInteraction(aliceStore, bobStore)

        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             self.__class__.BOB_RECIPIENT_ID,
                                             1)
        aliceSessionCipher = SessionCipher(aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           self.__class__.BOB_RECIPIENT_ID,
                                           1)

        bobPreKeyPair = Curve.generateKeyPair()
        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(),
                                 1, 31338, bobPreKeyPair.getPublicKey(),
                                 0, None, None, bobStore.getIdentityKeyPair().getPublicKey())

        bobStore.storePreKey(31338, PreKeyRecord(bobPreKey.getPreKeyId(), bobPreKeyPair))
        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

        outgoingMessage = aliceSessionCipher.encrypt(originalMessage)
        try:
            bobSessionCipher.decryptPkmsg(PreKeyWhisperMessage(serialized=outgoingMessage.serialize()))
            raise AssertionError("shouldn't be trusted!")
        except Exception:
            bobStore.saveIdentity(self.__class__.ALICE_RECIPIENT_ID,
                                  PreKeyWhisperMessage(serialized=outgoingMessage.serialize()).getIdentityKey())

        plaintext = bobSessionCipher.decryptPkmsg(PreKeyWhisperMessage(serialized=outgoingMessage.serialize()))
        if sys.version_info >= (3,0): plaintext = plaintext.decode()
        self.assertEqual(plaintext, originalMessage)

        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1,
                                 31337, Curve.generateKeyPair().getPublicKey(),
                                 0, None, None,
                                 aliceStore.getIdentityKeyPair().getPublicKey())
        try:
            aliceSessionBuilder.processPreKeyBundle(bobPreKey)
            raise AssertionError("shouldn't be trusted")
        except Exception:
            # good
            pass

        return

    def test_basicPreKeyV3(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             self.__class__.BOB_RECIPIENT_ID,
                                             1)

        bobStore = InMemoryAxolotlStore()
        bobPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeySignature = Curve.calculateSignature(bobStore.getIdentityKeyPair().getPrivateKey(),
                                                            bobSignedPreKeyPair.getPublicKey().serialize())

        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1, 31337, bobPreKeyPair.getPublicKey(),
                                 22, bobSignedPreKeyPair.getPublicKey(), bobSignedPreKeySignature,
                                 bobStore.getIdentityKeyPair().getPublicKey())

        aliceSessionBuilder.processPreKeyBundle(bobPreKey)
        self.assertTrue(aliceStore.containsSession(self.__class__.BOB_RECIPIENT_ID, 1))
        self.assertTrue(aliceStore.loadSession(self.__class__.BOB_RECIPIENT_ID,
                                               1).getSessionState().getSessionVersion() == 3)

        originalMessage = "L'homme est condamné à être libre"
        aliceSessionCipher = SessionCipher(aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           self.__class__.BOB_RECIPIENT_ID,
                                           1)
        outgoingMessage = aliceSessionCipher.encrypt(originalMessage)

        self.assertTrue(outgoingMessage.getType() == CiphertextMessage.PREKEY_TYPE)

        incomingMessage = PreKeyWhisperMessage(serialized=outgoingMessage.serialize())
        bobStore.storePreKey(31337, PreKeyRecord(bobPreKey.getPreKeyId(), bobPreKeyPair))
        bobStore.storeSignedPreKey(22, SignedPreKeyRecord(22,
                                                          int(time.time() * 1000),
                                                          bobSignedPreKeyPair,
                                                          bobSignedPreKeySignature))

        bobSessionCipher = SessionCipher(bobStore, bobStore, bobStore, bobStore, self.__class__.ALICE_RECIPIENT_ID, 1)

        plaintext = bobSessionCipher.decryptPkmsg(incomingMessage)
        if sys.version_info >= (3,0): plaintext = plaintext.decode()
        self.assertEqual(originalMessage, plaintext)
        # @@TODO: in callback assertion
        # self.assertFalse(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))

        self.assertTrue(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))

        self.assertTrue(bobStore.loadSession(self.__class__.ALICE_RECIPIENT_ID,
                                             1).getSessionState().getSessionVersion() == 3)
        self.assertTrue(bobStore.loadSession(self.__class__.ALICE_RECIPIENT_ID,
                                             1).getSessionState().getAliceBaseKey() is not None)
        self.assertEqual(originalMessage, plaintext)

        bobOutgoingMessage = bobSessionCipher.encrypt(originalMessage)
        self.assertTrue(bobOutgoingMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        alicePlaintext = aliceSessionCipher.decryptMsg(WhisperMessage(serialized=bobOutgoingMessage.serialize()))
        if sys.version_info >= (3,0): alicePlaintext = alicePlaintext.decode()
        self.assertEqual(alicePlaintext, originalMessage)

        self.runInteraction(aliceStore, bobStore)

        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             self.__class__.BOB_RECIPIENT_ID,
                                             1)
        aliceSessionCipher = SessionCipher(aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           self.__class__.BOB_RECIPIENT_ID,
                                           1)

        bobPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeySignature = Curve.calculateSignature(bobStore.getIdentityKeyPair().getPrivateKey(),
                                                            bobSignedPreKeyPair.getPublicKey().serialize())
        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1, 31338, bobPreKeyPair.getPublicKey(),
                                 23, bobSignedPreKeyPair.getPublicKey(), bobSignedPreKeySignature,
                                 bobStore.getIdentityKeyPair().getPublicKey())

        bobStore.storePreKey(31338, PreKeyRecord(bobPreKey.getPreKeyId(), bobPreKeyPair))
        bobStore.storeSignedPreKey(23, SignedPreKeyRecord(23,
                                                          int(time.time() * 1000),
                                                          bobSignedPreKeyPair,
                                                          bobSignedPreKeySignature))
        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

        outgoingMessage = aliceSessionCipher.encrypt(originalMessage)

        try:
            plaintext = bobSessionCipher.decryptPkmsg(PreKeyWhisperMessage(serialized=outgoingMessage))
            raise AssertionError("shouldn't be trusted!")
        except Exception:
            bobStore.saveIdentity(self.__class__.ALICE_RECIPIENT_ID,
                                  PreKeyWhisperMessage(serialized=outgoingMessage.serialize()).getIdentityKey())

        plaintext = bobSessionCipher.decryptPkmsg(PreKeyWhisperMessage(serialized=outgoingMessage.serialize()))
        if sys.version_info >= (3,0): plaintext = plaintext.decode()
        self.assertEqual(plaintext, originalMessage)

        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1, 31337,
                                 Curve.generateKeyPair().getPublicKey(), 23, bobSignedPreKeyPair.getPublicKey(),
                                 bobSignedPreKeySignature, aliceStore.getIdentityKeyPair().getPublicKey())
        try:
            aliceSessionBuilder.process(bobPreKey)
            raise AssertionError("shouldn't be trusted!")
        except Exception:
            # good
            pass

    def test_badSignedPreKeySignature(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore, aliceStore, aliceStore, aliceStore,
                                             self.__class__.BOB_RECIPIENT_ID, 1)

        bobIdentityKeyStore = InMemoryIdentityKeyStore()

        bobPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeySignature = Curve.calculateSignature(bobIdentityKeyStore.getIdentityKeyPair().getPrivateKey(),
                                                            bobSignedPreKeyPair.getPublicKey().serialize())

        for i in range(0, len(bobSignedPreKeySignature) * 8):
            modifiedSignature = bytearray(bobSignedPreKeySignature[:])
            modifiedSignature[int(i/8)] ^= 0x01 << (i % 8)

            bobPreKey = PreKeyBundle(bobIdentityKeyStore.getLocalRegistrationId(), 1, 31337,
                                     bobPreKeyPair.getPublicKey(), 22, bobSignedPreKeyPair.getPublicKey(),
                                     modifiedSignature, bobIdentityKeyStore.getIdentityKeyPair().getPublicKey())

            try:
                aliceSessionBuilder.processPreKeyBundle(bobPreKey)
            except Exception:
                # good
                pass
        bobPreKey = PreKeyBundle(bobIdentityKeyStore.getLocalRegistrationId(), 1, 31337,
                                 bobPreKeyPair.getPublicKey(), 22, bobSignedPreKeyPair.getPublicKey(),
                                 bobSignedPreKeySignature, bobIdentityKeyStore.getIdentityKeyPair().getPublicKey())

        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

    def test_basicKeyExchange(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             self.__class__.BOB_RECIPIENT_ID,
                                             1)

        bobStore = InMemoryAxolotlStore()
        bobSessionBuilder = SessionBuilder(bobStore,
                                           bobStore,
                                           bobStore,
                                           bobStore,
                                           self.__class__.ALICE_RECIPIENT_ID,
                                           1)

        aliceKeyExchangeMessage = aliceSessionBuilder.processInitKeyExchangeMessage()
        self.assertTrue(aliceKeyExchangeMessage is not None)

        aliceKeyExchangeMessageBytes = aliceKeyExchangeMessage.serialize()
        bobKeyExchangeMessage = bobSessionBuilder.processKeyExchangeMessage(KeyExchangeMessage(
            serialized=aliceKeyExchangeMessageBytes))

        self.assertTrue(bobKeyExchangeMessage is not None)

        bobKeyExchangeMessageBytes = bobKeyExchangeMessage.serialize()
        response = aliceSessionBuilder.processKeyExchangeMessage(KeyExchangeMessage(
            serialized=bobKeyExchangeMessageBytes))

        self.assertTrue(response is None)
        self.assertTrue(aliceStore.containsSession(self.__class__.BOB_RECIPIENT_ID, 1))
        self.assertTrue(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))

        self.runInteraction(aliceStore, bobStore)

        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             aliceStore,
                                             self.__class__.BOB_RECIPIENT_ID,
                                             1)
        aliceKeyExchangeMessage = aliceSessionBuilder.processInitKeyExchangeMessage()

        try:
            bobKeyExchangeMessage = bobSessionBuilder.processKeyExchangeMessage(aliceKeyExchangeMessage)
            raise AssertionError("This identity shouldn't be trusted!")
        except UntrustedIdentityException:
            bobStore.saveIdentity(self.__class__.ALICE_RECIPIENT_ID, aliceKeyExchangeMessage.getIdentityKey())
        bobKeyExchangeMessage = bobSessionBuilder.processKeyExchangeMessage(aliceKeyExchangeMessage)

        self.assertTrue(aliceSessionBuilder.processKeyExchangeMessage(bobKeyExchangeMessage) == None)

        self.runInteraction(aliceStore, bobStore)

    def runInteraction(self, aliceStore, bobStore):
        """
        :type aliceStore: AxolotlStore
        :type  bobStore: AxolotlStore
        """
        aliceSessionCipher = SessionCipher(aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           aliceStore,
                                           self.__class__.BOB_RECIPIENT_ID,
                                           1)
        bobSessionCipher = SessionCipher(bobStore, bobStore, bobStore, bobStore, self.__class__.ALICE_RECIPIENT_ID, 1)

        originalMessage = "smert ze smert"
        aliceMessage = aliceSessionCipher.encrypt(originalMessage)

        self.assertTrue(aliceMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        plaintext = bobSessionCipher.decryptMsg(WhisperMessage(serialized=aliceMessage.serialize()))
        if sys.version_info >= (3,0): plaintext = plaintext.decode()
        self.assertEqual(plaintext, originalMessage)

        bobMessage = bobSessionCipher.encrypt(originalMessage)

        self.assertTrue(bobMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        plaintext = aliceSessionCipher.decryptMsg(WhisperMessage(serialized=bobMessage.serialize()))
        if sys.version_info >= (3,0): plaintext = plaintext.decode()
        self.assertEqual(plaintext, originalMessage)

        for i in range(0, 10):
            loopingMessage = "What do we mean by saying that existence precedes essence? " \
                             "We mean that man first of all exists, encounters himself, " \
                             "surges up in the world--and defines himself aftward. %s" % i
            aliceLoopingMessage = aliceSessionCipher.encrypt(loopingMessage)
            loopingPlaintext = bobSessionCipher.decryptMsg(WhisperMessage(serialized=aliceLoopingMessage.serialize()))
            if sys.version_info >= (3,0): loopingPlaintext = loopingPlaintext.decode()
            self.assertEqual(loopingPlaintext, loopingMessage)

        for i in range(0, 10):
            loopingMessage = "What do we mean by saying that existence precedes essence? " \
                 "We mean that man first of all exists, encounters himself, " \
                 "surges up in the world--and defines himself aftward. %s" % i
            bobLoopingMessage = bobSessionCipher.encrypt(loopingMessage)

            loopingPlaintext = aliceSessionCipher.decryptMsg(WhisperMessage(serialized=bobLoopingMessage.serialize()))
            if sys.version_info >= (3,0): loopingPlaintext = loopingPlaintext.decode()
            self.assertEqual(loopingPlaintext, loopingMessage)

        aliceOutOfOrderMessages = []

        for i in range(0, 10):
            loopingMessage = "What do we mean by saying that existence precedes essence? " \
                 "We mean that man first of all exists, encounters himself, " \
                 "surges up in the world--and defines himself aftward. %s" % i
            aliceLoopingMessage = aliceSessionCipher.encrypt(loopingMessage)
            aliceOutOfOrderMessages.append((loopingMessage, aliceLoopingMessage))

        for i in range(0, 10):
            loopingMessage = "What do we mean by saying that existence precedes essence? " \
                 "We mean that man first of all exists, encounters himself, " \
                 "surges up in the world--and defines himself aftward. %s" % i
            aliceLoopingMessage = aliceSessionCipher.encrypt(loopingMessage)
            loopingPlaintext = bobSessionCipher.decryptMsg(WhisperMessage(serialized=aliceLoopingMessage.serialize()))
            if sys.version_info >= (3,0): loopingPlaintext = loopingPlaintext.decode()
            self.assertEqual(loopingPlaintext, loopingMessage)

        for i in range(0, 10):
            loopingMessage = "You can only desire based on what you know: %s" % i
            bobLoopingMessage = bobSessionCipher.encrypt(loopingMessage)

            loopingPlaintext = aliceSessionCipher.decryptMsg(WhisperMessage(serialized=bobLoopingMessage.serialize()))
            if sys.version_info >= (3,0): loopingPlaintext = loopingPlaintext.decode()
            self.assertEqual(loopingPlaintext, loopingMessage)

        for aliceOutOfOrderMessage in aliceOutOfOrderMessages:
            outOfOrderPlaintext = bobSessionCipher.decryptMsg(WhisperMessage(
                serialized=aliceOutOfOrderMessage[1].serialize()))
            if sys.version_info >= (3,0): outOfOrderPlaintext = outOfOrderPlaintext.decode()
            self.assertEqual(outOfOrderPlaintext, aliceOutOfOrderMessage[0])
