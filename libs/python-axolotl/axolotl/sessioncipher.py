# -*- coding: utf-8 -*-

import sys

import Crypto.Cipher.AES as AES
from Crypto.Util import Counter

from .ecc.curve import Curve
from .sessionbuilder import SessionBuilder
from .util.byteutil import ByteUtil
from .state.sessionstate import SessionState
from .protocol.whispermessage import WhisperMessage
from .protocol.prekeywhispermessage import PreKeyWhisperMessage
from .nosessionexception import NoSessionException
from .invalidmessageexception import InvalidMessageException
from .duplicatemessagexception import DuplicateMessageException


if sys.version_info >= (3, 0):
    unicode = str

import  logging
logger = logging.getLogger(__name__)
class SessionCipher:
    def __init__(self, sessionStore, preKeyStore, signedPreKeyStore, identityKeyStore, recepientId, deviceId):
        self.sessionStore = sessionStore
        self.preKeyStore = preKeyStore
        self.recipientId = recepientId
        self.deviceId = deviceId
        self.sessionBuilder = SessionBuilder(sessionStore, preKeyStore, signedPreKeyStore,
                                             identityKeyStore, recepientId, deviceId)

    def encrypt(self, paddedMessage):
        """
        :type paddedMessage: str
        """
        # TODO: make this less ugly and python 2 and 3 compatible
        # paddedMessage = bytearray(paddedMessage.encode() if (sys.version_info >= (3, 0) and not type(paddedMessage) in (bytes, bytearray)) or type(paddedMessage) is unicode else paddedMessage)
        if (sys.version_info >= (3, 0) and
                not type(paddedMessage) in (bytes, bytearray)) or type(paddedMessage) is unicode:
            paddedMessage = bytearray(paddedMessage.encode())
        else:
            paddedMessage = bytearray(paddedMessage)

        sessionRecord = self.sessionStore.loadSession(self.recipientId, self.deviceId)
        sessionState = sessionRecord.getSessionState()
        chainKey = sessionState.getSenderChainKey()
        messageKeys = chainKey.getMessageKeys()
        senderEphemeral = sessionState.getSenderRatchetKey()
        previousCounter = sessionState.getPreviousCounter()
        sessionVersion = sessionState.getSessionVersion()

        ciphertextBody = self.getCiphertext(sessionVersion, messageKeys, paddedMessage)
        ciphertextMessage = WhisperMessage(sessionVersion, messageKeys.getMacKey(),
                                           senderEphemeral, chainKey.getIndex(),
                                           previousCounter, ciphertextBody,
                                           sessionState.getLocalIdentityKey(),
                                           sessionState.getRemoteIdentityKey())

        if sessionState.hasUnacknowledgedPreKeyMessage():
            items = sessionState.getUnacknowledgedPreKeyMessageItems()
            localRegistrationid = sessionState.getLocalRegistrationId()

            ciphertextMessage = PreKeyWhisperMessage(sessionVersion, localRegistrationid, items.getPreKeyId(),
                                                     items.getSignedPreKeyId(), items.getBaseKey(),
                                                     sessionState.getLocalIdentityKey(),
                                                     ciphertextMessage)
        sessionState.setSenderChainKey(chainKey.getNextChainKey())
        self.sessionStore.storeSession(self.recipientId, self.deviceId, sessionRecord)

        return ciphertextMessage

    def decryptMsg(self, ciphertext, textMsg=True):
        """
        :type ciphertext: WhisperMessage
        :type textMsg: Bool set this to False if you are decrypting bytes
                       instead of string
        """

        if not self.sessionStore.containsSession(self.recipientId, self.deviceId):
            raise NoSessionException("No session for: %s, %s" % (self.recipientId, self.deviceId))

        sessionRecord = self.sessionStore.loadSession(self.recipientId, self.deviceId)
        plaintext = self.decryptWithSessionRecord(sessionRecord, ciphertext)

        self.sessionStore.storeSession(self.recipientId, self.deviceId, sessionRecord)

        return plaintext

    def decryptPkmsg(self, ciphertext, textMsg=True):
        """
        :type ciphertext: PreKeyWhisperMessage
        """
        sessionRecord = self.sessionStore.loadSession(self.recipientId, self.deviceId)
        unsignedPreKeyId = self.sessionBuilder.process(sessionRecord, ciphertext)
        plaintext = self.decryptWithSessionRecord(sessionRecord, ciphertext.getWhisperMessage())

        # callback.handlePlaintext(plaintext)
        self.sessionStore.storeSession(self.recipientId, self.deviceId, sessionRecord)

        if unsignedPreKeyId is not None:
            self.preKeyStore.removePreKey(unsignedPreKeyId)

        return plaintext

    def decryptWithSessionRecord(self, sessionRecord, cipherText):
        """
        :type sessionRecord: SessionRecord
        :type cipherText: WhisperMessage
        """

        previousStates = sessionRecord.getPreviousSessionStates()
        exceptions = []
        try:
            sessionState = SessionState(sessionRecord.getSessionState())
            plaintext = self.decryptWithSessionState(sessionState, cipherText)
            sessionRecord.setState(sessionState)
            return plaintext
        except InvalidMessageException as e:
            exceptions.append(e)

        for i in range(0, len(previousStates)):
            previousState = previousStates[i]
            try:
                promotedState = SessionState(previousState)
                plaintext = self.decryptWithSessionState(promotedState, cipherText)
                previousStates.pop(i)
                sessionRecord.promoteState(promotedState)
                return plaintext
            except InvalidMessageException as e:
                exceptions.append(e)

        raise InvalidMessageException("No valid sessions", exceptions)

    def decryptWithSessionState(self, sessionState, ciphertextMessage):

        if not sessionState.hasSenderChain():
            raise InvalidMessageException("Uninitialized session!")

        if ciphertextMessage.getMessageVersion() != sessionState.getSessionVersion():
            raise InvalidMessageException("Message version %s, but session version %s" % (ciphertextMessage.getMessageVersion, sessionState.getSessionVersion()))

        messageVersion = ciphertextMessage.getMessageVersion()
        theirEphemeral = ciphertextMessage.getSenderRatchetKey()
        counter = ciphertextMessage.getCounter()
        chainKey = self.getOrCreateChainKey(sessionState, theirEphemeral)
        messageKeys = self.getOrCreateMessageKeys(sessionState, theirEphemeral, chainKey, counter)

        ciphertextMessage.verifyMac(messageVersion,
                                    sessionState.getRemoteIdentityKey(),
                                    sessionState.getLocalIdentityKey(),
                                    messageKeys.getMacKey())

        plaintext = self.getPlaintext(messageVersion, messageKeys, ciphertextMessage.getBody())
        sessionState.clearUnacknowledgedPreKeyMessage()

        return plaintext

    def getOrCreateChainKey(self, sessionState, ECPublickKey_theirEphemeral):
        theirEphemeral = ECPublickKey_theirEphemeral
        if sessionState.hasReceiverChain(theirEphemeral):
            return sessionState.getReceiverChainKey(theirEphemeral)
        else:
            rootKey = sessionState.getRootKey()
            ourEphemeral = sessionState.getSenderRatchetKeyPair()
            receiverChain = rootKey.createChain(theirEphemeral, ourEphemeral)
            ourNewEphemeral = Curve.generateKeyPair()
            senderChain = receiverChain[0].createChain(theirEphemeral, ourNewEphemeral)

            sessionState.setRootKey(senderChain[0])
            sessionState.addReceiverChain(theirEphemeral, receiverChain[1])
            sessionState.setPreviousCounter(max(sessionState.getSenderChainKey().getIndex() - 1, 0))
            sessionState.setSenderChain(ourNewEphemeral, senderChain[1])
            return receiverChain[1]

    def getOrCreateMessageKeys(self, sessionState, ECPublicKey_theirEphemeral, chainKey, counter):
        theirEphemeral = ECPublicKey_theirEphemeral
        if chainKey.getIndex() > counter:
            if sessionState.hasMessageKeys(theirEphemeral, counter):
                return sessionState.removeMessageKeys(theirEphemeral, counter)
            else:
                raise DuplicateMessageException("Received message with old counter: %s, %s" % (chainKey.getIndex(),
                                                                                               counter))

        if counter - chainKey.getIndex() > 2000:
            raise InvalidMessageException("Over 2000 messages into the future!")

        while chainKey.getIndex() < counter:
            messageKeys = chainKey.getMessageKeys()
            sessionState.setMessageKeys(theirEphemeral, messageKeys)
            chainKey = chainKey.getNextChainKey()

        sessionState.setReceiverChainKey(theirEphemeral, chainKey.getNextChainKey())
        return chainKey.getMessageKeys()

    def getCiphertext(self, version, messageKeys, plainText):
        """
        :type version: int
        :type messageKeys: MessageKeys
        :type  plainText: bytearray
        """
        cipher = None
        if version >= 3:
            cipher = self.getCipher(messageKeys.getCipherKey(), messageKeys.getIv())
        else:
            cipher = self.getCipher_v2(messageKeys.getCipherKey(), messageKeys.getCounter())

        return cipher.encrypt(bytes(plainText))

    def getPlaintext(self, version, messageKeys, cipherText):
        cipher = None
        if version >= 3:
            cipher = self.getCipher(messageKeys.getCipherKey(), messageKeys.getIv())
        else:
            cipher = self.getCipher_v2(messageKeys.getCipherKey(), messageKeys.getCounter())

        return cipher.decrypt(cipherText)

    def getCipher(self, key, iv):
        # Cipher.getInstance("AES/CBC/PKCS5Padding");
        # cipher = AES.new(key, AES.MODE_CBC, IV = iv)
        # return cipher
        return AESCipher(key, iv)

    def getCipher_v2(self, key, counter):
        # AES/CTR/NoPadding
        # counterbytes = struct.pack('>L', counter) + (b'\x00' * 12)
        # counterint = struct.unpack(">L", counterbytes)[0]
        # counterint = int.from_bytes(counterbytes, byteorder='big')
        ctr = Counter.new(128, initial_value=counter)

        # cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        ivBytes = bytearray(16)
        ByteUtil.intToByteArray(ivBytes, 0, counter)

        cipher = AES.new(key, AES.MODE_CTR, IV=bytes(ivBytes), counter=ctr)

        return cipher


BS = 16
if sys.version_info >= (3, 0):
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    unpad = lambda s : s[0:-s[-1]]
else:
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s : s[0:-ord(s[-1])]


class AESCipher:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.cipher = AES.new(key, AES.MODE_CBC, IV = iv)

    def unpad(self, data):
        unpadLength = data[-1]
        if type(unpadLength) is int:
            cmp = bytes([data[-unpadLength]] * unpadLength)
        else:
            unpadLength = ord(unpadLength)
            cmp = data[-unpadLength] * unpadLength
        if data[-unpadLength:] != cmp:
            raise ValueError("Data not properly padded \n %s" %  data)

        return data[0:-unpadLength]

    def encrypt(self, raw):
        # if sys.version_info >= (3,0):
        #     rawPadded = pad(raw.decode()).encode()
        # else:
        rawPadded = pad(raw)
        try:
            return self.cipher.encrypt(rawPadded)
        except ValueError:
            raise

    def decrypt(self, enc):
        return self.unpad(self.cipher.decrypt(enc))
