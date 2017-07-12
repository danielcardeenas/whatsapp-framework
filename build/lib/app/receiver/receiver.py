from app.utils import helper
receivers = []


class Receiver(object):
    def __init__(self, identifier, conversation, creator, fn=None):
        self.identifier = identifier
        self.conversation = conversation
        self.creator = creator
        self.fn = fn
        receivers.append(self)
        
    def destroy(self):
        receivers[:] = [receiver for receiver in receivers 
                            if not receiver == self]


def intercept(self, message_entity):
    if intercept_with_identifier(message_entity):
        print("Handling identifier")

    if receivers_have_global():
        print("Handling globals")
        handle_global_receivers(message_entity)
        

def intercept_with_identifier(message_entity):
    if len(receivers) == 0:
        return False

    # Get receiver if any
    receiver = get_receiver(message_entity)
    
    if receiver:
        print("Found receiver with id: " + receiver.identifier)
        receiver.fn(message_entity)
        return True
    else:
        return False

def receivers_have_global():
    for receiver in receivers:
        if receiver.identifier == "__global__":
            return True

    return False


def handle_global_receivers(message_entity):
    for receiver in receivers:
        if receiver.identifier == "__global__":
            if helper.get_conversation(message_entity) == receiver.conversation:
                receiver.fn(message_entity)


def get_receiver(message_entity):
    for receiver in receivers:
        message = message_entity.getBody()
        if receiver.identifier in message: 
            # Matches identifier. Check if it belongs to the same conversation
            if helper.get_conversation(message_entity) == receiver.conversation:
                return receiver

    return None
