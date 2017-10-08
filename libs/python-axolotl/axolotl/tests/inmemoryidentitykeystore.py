# -*- coding: utf-8 -*-

from ..state.identitykeystore import IdentityKeyStore
from ..ecc.curve import Curve
from ..identitykey import IdentityKey
from ..util.keyhelper import KeyHelper
from ..identitykeypair import IdentityKeyPair


class InMemoryIdentityKeyStore(IdentityKeyStore):
    def __init__(self):
        self.trustedKeys = {}
        identityKeyPairKeys = Curve.generateKeyPair()
        self.identityKeyPair = IdentityKeyPair(IdentityKey(identityKeyPairKeys.getPublicKey()),
                                               identityKeyPairKeys.getPrivateKey())
        self.localRegistrationId = KeyHelper.generateRegistrationId()

    def getIdentityKeyPair(self):
        return self.identityKeyPair

    def getLocalRegistrationId(self):
        return self.localRegistrationId

    def saveIdentity(self, recepientId, identityKey):
        self.trustedKeys[recepientId] = identityKey

    def isTrustedIdentity(self, recepientId, identityKey):
        if recepientId not in self.trustedKeys:
            return True
        return self.trustedKeys[recepientId] == identityKey
