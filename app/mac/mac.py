from yowsup.layers.protocol_presence.protocolentities import *

ack_queue = []


def disconnect(self):
    self.toLower(UnavailablePresenceProtocolEntity())


def ack_messages(self, conversation):
    # Filter messages from this conversation
    queue = [message_entity for message_entity in conversation if same_conversation(message_entity, conversation)]

    # Get only last 10 messages (Will discard reading the others)
    queue = queue[-10:]

    # Ack every message in queue
    for message_entity in queue:
        self.toLower(message_entity.ack(True))

        # Remove it from queue
        if message_entity in ack_queue:
            ack_queue.remove(message_entity)

    # Clean queue
    remove_conversation_from_queue(conversation)


def same_conversation(message_entity, conversation):
    return message_entity.getFrom() == conversation


def remove_conversation_from_queue(conversation):
    ack_queue[:] = [entity for entity in ack_queue if not same_conversation(entity, conversation)]
