from app.utils import helper

class Voter(object):
    def __init__(self, message_entity):
        self.who = helper.get_who_send(message_entity)
        self.conversation = message_entity.getFrom()
        self.who_name = helper.sender_name(message_entity)