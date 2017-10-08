# -*- coding: utf-8 -*-

import abc

from .identitykeystore import IdentityKeyStore
from .prekeystore import PreKeyStore
from .sessionstore import SessionStore
from .signedprekeystore import SignedPreKeyStore


class AxolotlStore(IdentityKeyStore, PreKeyStore, SignedPreKeyStore, SessionStore):
    __metaclass__ = abc.ABCMeta
