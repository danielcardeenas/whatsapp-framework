from app.utils import helper
receivers = []


class Receiver(object):
    def __init__(self, identifier, creator, fn=None):
        self.identifier = identifier
        self.creator = creator
        self.fn = fn
        receivers.append(self)


def intercept(self, message_entity):
    if should_intercept(message_entity):
        print("Handling identifier")

    if receivers_have_global():
        print("Handling globals")
        handle_global_receivers(message_entity)


def should_intercept(message_entity):
    if len(receivers) == 0:
        return False

    # Get receiver if any
    receiver = message_has_identifier(message_entity)
    if receiver:
        print("Found receiver with id: " + receiver.identifier)
        receiver.fn(message_entity)
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
            receiver.fn(message_entity)


def message_has_identifier(message_entity):
    for receiver in receivers:
        message = helper.clean_message(message_entity)
        id_len = len(receiver.identifier)
        if message[:id_len] == receiver.identifier:
            return receiver

    return None


def destroy_receivers(identifier):
    print("Destroying receivers with identifier: " + identifier)