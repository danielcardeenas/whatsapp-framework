# -*- coding: utf-8 -*-

class UntrustedIdentityException(Exception):
    def __init__(self, name, identityKey):
        self.name = name
        self.identityKey = identityKey

    def getName(self):
        return self.name

    def getIdentityKey(self):
        return self.identityKey
