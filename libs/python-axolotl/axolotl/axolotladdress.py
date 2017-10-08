class AxolotlAddress(object):
    def __init__(self, name, deviceId):
        self.name = name
        self.deviceId = deviceId

    def getName(self):
        return self.name

    def getDeviceId(self):
        return self.deviceId

    def __str__(self):
        return "%s;%s" % (self.name, self.deviceId)

    def __eq__(self, other):
        if other is None:
            return False

        if other.__class__ != AxolotlAddress:
            return False

        return self.name == other.getName() and self.deviceId == other.getDeviceId()

    def __hash__(self):
        return hash(self.name) ^ self.deviceId
