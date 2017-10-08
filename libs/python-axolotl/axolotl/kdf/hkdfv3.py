# -*- codsing: utf-8 -*-

from .hkdf import HKDF


class HKDFv3(HKDF):
    def getIterationStartOffset(self):
        return 1
