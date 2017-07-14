from app.utils import helper

class Message(object):
    def __init__(self, message_entity):
        self.message = helper.clean_message(message_entity)
        self.who = helper.get_who_send(message_entity)
        self.conversation = message_entity.getFrom()
        self.message_entity = message_entity
        
        # These two attributes are just easier ways to identify instructions
        # But they are not really needed since you have the whole message
        # But I use these a lot so fuck it, lemme be happy
        # ===================================================================
        # command is what goes after '!'
        self.command = helper.command(message_entity)
        # predicate is what goes after the command
        self.predicate = helper.predicate(message_entity)