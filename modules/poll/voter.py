from app.utils import helper

class Voter(object):
    def __init__(self, message):
        self.who = message.who
        self.conversation = message.conversation
        self.who_name = message.who_name