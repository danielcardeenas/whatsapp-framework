class SenderKeyName(object):
    def __init__(self, groupId, senderAxolotlAddress):
        self.groupId = groupId
        self.sender = senderAxolotlAddress

    def getGroupId(self):
        return self.groupId

    def getSender(self):
        return self.sender

    def serialize(self):
        return "%s::%s::%s" % (self.groupId, self.sender.getName(), self.sender.getDeviceId())

    def __eq__(self, other):
        if other is None: return False
        if other.__class__ != SenderKeyName: return False

        return self.groupId == other.getGroupId() and self.sender == other.getSender()

    def __hash__(self):
        return hash(self.groupId) ^ hash(self.sender)
