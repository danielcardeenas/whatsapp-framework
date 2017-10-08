# -*- coding: utf-8 -*-

import unittest
import sys

from ..state.sessionrecord import SessionRecord
from ..ecc.curve import Curve
from ..identitykeypair import IdentityKeyPair, IdentityKey
from ..ratchet.aliceaxolotlparameters import AliceAxolotlParameters
from ..ratchet.bobaxolotlparamaters import BobAxolotlParameters
from ..ratchet.ratchetingsession import RatchetingSession
from ..tests.inmemoryaxolotlstore import InMemoryAxolotlStore
from ..sessioncipher import SessionCipher
from ..protocol.whispermessage import WhisperMessage


class SessionCipherTest(unittest.TestCase):
    def test_basicSessionV2(self):
        aliceSessionRecord = SessionRecord()
        bobSessionRecord = SessionRecord()
        self.initializeSessionsV2(aliceSessionRecord.getSessionState(), bobSessionRecord.getSessionState())
        self.runInteraction(aliceSessionRecord, bobSessionRecord)

    def test_basicSessionV3(self):
        aliceSessionRecord = SessionRecord()
        bobSessionRecord = SessionRecord()
        self.initializeSessionsV3(aliceSessionRecord.getSessionState(), bobSessionRecord.getSessionState())
        self.runInteraction(aliceSessionRecord, bobSessionRecord)

    def runInteraction(self, aliceSessionRecord, bobSessionRecord):
        aliceStore = InMemoryAxolotlStore()
        bobStore = InMemoryAxolotlStore()

        aliceStore.storeSession(2, 1, aliceSessionRecord)
        bobStore.storeSession(3, 1, bobSessionRecord)

        aliceCipher = SessionCipher(aliceStore, aliceStore, aliceStore, aliceStore, 2, 1)
        bobCipher = SessionCipher(bobStore, bobStore, bobStore, bobStore, 3, 1)

        alicePlaintext = "This is a plaintext message."
        message = aliceCipher.encrypt(alicePlaintext)
        bobPlaintext = bobCipher.decryptMsg(WhisperMessage(serialized=message.serialize()))

        if sys.version_info >= (3,0): bobPlaintext = bobPlaintext.decode()
        self.assertEqual(alicePlaintext, bobPlaintext)

        bobReply = "This is a message from Bob."
        reply = bobCipher.encrypt(bobReply)
        receivedReply = aliceCipher.decryptMsg(WhisperMessage(serialized=reply.serialize()))
        if sys.version_info >= (3,0): receivedReply = receivedReply.decode()

        self.assertEqual(bobReply, receivedReply)

        aliceCiphertextMessages = []
        alicePlaintextMessages = []

        for i in range(0, 50):
            alicePlaintextMessages.append("смерть за смерть %s" % i)
            aliceCiphertextMessages.append(aliceCipher.encrypt("смерть за смерть %s" % i))

        # shuffle(aliceCiphertextMessages)
        # shuffle(alicePlaintextMessages)

        for i in range(0, int(len(aliceCiphertextMessages)/2)):
            receivedPlaintext = bobCipher.decryptMsg(WhisperMessage(serialized=aliceCiphertextMessages[i].serialize()))
            self.assertEqual(receivedPlaintext.decode() if sys.version_info >= (3,0) else receivedPlaintext, alicePlaintextMessages[i])

        """

    List<CiphertextMessage> bobCiphertextMessages = new ArrayList<>();
    List<byte[]>            bobPlaintextMessages  = new ArrayList<>();

    for (int i=0;i<20;i++) {
      bobPlaintextMessages.add(("смерть за смерть " + i).getBytes());
      bobCiphertextMessages.add(bobCipher.encrypt(("смерть за смерть " + i).getBytes()));
    }

    seed = System.currentTimeMillis();

    Collections.shuffle(bobCiphertextMessages, new Random(seed));
    Collections.shuffle(bobPlaintextMessages, new Random(seed));

    for (int i=0;i<bobCiphertextMessages.size() / 2;i++) {
      byte[] receivedPlaintext = aliceCipher.decrypt(new WhisperMessage(bobCiphertextMessages.get(i).serialize()));
      assertTrue(Arrays.equals(receivedPlaintext, bobPlaintextMessages.get(i)));
    }

    for (int i=aliceCiphertextMessages.size()/2;i<aliceCiphertextMessages.size();i++) {
      byte[] receivedPlaintext = bobCipher.decrypt(new WhisperMessage(aliceCiphertextMessages.get(i).serialize()));
      assertTrue(Arrays.equals(receivedPlaintext, alicePlaintextMessages.get(i)));
    }

    for (int i=bobCiphertextMessages.size() / 2;i<bobCiphertextMessages.size();i++) {
      byte[] receivedPlaintext = aliceCipher.decrypt(new WhisperMessage(bobCiphertextMessages.get(i).serialize()));
      assertTrue(Arrays.equals(receivedPlaintext, bobPlaintextMessages.get(i)));
    }
        """

    def initializeSessionsV2(self, aliceSessionState, bobSessionState):
        aliceIdentityKeyPair = Curve.generateKeyPair()
        aliceIdentityKey = IdentityKeyPair(IdentityKey(aliceIdentityKeyPair.getPublicKey()),
                                           aliceIdentityKeyPair.getPrivateKey())
        aliceBaseKey = Curve.generateKeyPair()
        # aliceEphemeralKey = Curve.generateKeyPair()

        bobIdentityKeyPair = Curve.generateKeyPair()
        bobIdentityKey = IdentityKeyPair(IdentityKey(bobIdentityKeyPair.getPublicKey()),
                                         bobIdentityKeyPair.getPrivateKey())
        bobBaseKey = Curve.generateKeyPair()
        bobEphemeralKey = bobBaseKey

        aliceParameters = AliceAxolotlParameters.newBuilder()\
            .setOurIdentityKey(aliceIdentityKey)\
            .setOurBaseKey(aliceBaseKey)\
            .setTheirIdentityKey(bobIdentityKey.getPublicKey())\
            .setTheirSignedPreKey(bobEphemeralKey.getPublicKey())\
            .setTheirRatchetKey(bobEphemeralKey.getPublicKey())\
            .setTheirOneTimePreKey(None)\
            .create()

        bobParameters = BobAxolotlParameters.newBuilder()\
            .setOurIdentityKey(bobIdentityKey)\
            .setOurOneTimePreKey(None)\
            .setOurRatchetKey(bobEphemeralKey)\
            .setOurSignedPreKey(bobBaseKey)\
            .setTheirBaseKey(aliceBaseKey.getPublicKey())\
            .setTheirIdentityKey(aliceIdentityKey.getPublicKey())\
            .create()

        RatchetingSession.initializeSessionAsAlice(aliceSessionState, 2, aliceParameters)
        RatchetingSession.initializeSessionAsBob(bobSessionState, 2, bobParameters)

    def initializeSessionsV3(self, aliceSessionState, bobSessionState):
        aliceIdentityKeyPair = Curve.generateKeyPair()
        aliceIdentityKey = IdentityKeyPair(IdentityKey(aliceIdentityKeyPair.getPublicKey()),
                                           aliceIdentityKeyPair.getPrivateKey())
        aliceBaseKey = Curve.generateKeyPair()
        # aliceEphemeralKey = Curve.generateKeyPair()

        # alicePreKey = aliceBaseKey

        bobIdentityKeyPair = Curve.generateKeyPair()
        bobIdentityKey = IdentityKeyPair(IdentityKey(bobIdentityKeyPair.getPublicKey()),
                                         bobIdentityKeyPair.getPrivateKey())
        bobBaseKey = Curve.generateKeyPair()
        bobEphemeralKey = bobBaseKey

        # bobPreKey = Curve.generateKeyPair()

        aliceParameters = AliceAxolotlParameters.newBuilder()\
            .setOurBaseKey(aliceBaseKey)\
            .setOurIdentityKey(aliceIdentityKey)\
            .setTheirOneTimePreKey(None)\
            .setTheirRatchetKey(bobEphemeralKey.getPublicKey())\
            .setTheirSignedPreKey(bobBaseKey.getPublicKey())\
            .setTheirIdentityKey(bobIdentityKey.getPublicKey())\
            .create()

        bobParameters = BobAxolotlParameters.newBuilder()\
            .setOurRatchetKey(bobEphemeralKey)\
            .setOurSignedPreKey(bobBaseKey)\
            .setOurOneTimePreKey(None)\
            .setOurIdentityKey(bobIdentityKey)\
            .setTheirIdentityKey(aliceIdentityKey.getPublicKey())\
            .setTheirBaseKey(aliceBaseKey.getPublicKey())\
            .create()

        RatchetingSession.initializeSessionAsAlice(aliceSessionState, 3, aliceParameters)
        RatchetingSession.initializeSessionAsBob(bobSessionState, 3, bobParameters)
