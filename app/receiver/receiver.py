from app.utils import helper
receivers = []

class Receiver(object):
    def __init__(self, identifier, creator, fn=None):
        self.identifier = identifier
        self.creator = creator
        self.fn = fn
        receivers.append(self)