from app.utils import helper

class Receipt(object):
    def __init__(self, message_entity):
        self.who = message_entity.getParticipant()
        self.conversation = message_entity.getFrom()
        self.timestamp = message_entity.timestamp
        self.message_entity = message_entity
        self.blue = message_entity.type == "read"
        
    """
    Logs message node
    """
    def log(self, deep=False):
        helper.log(self)
        if deep:
            helper.log(self.message_entity)