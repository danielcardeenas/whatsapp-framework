from yowsup.layers.protocol_messages.protocolentities import *
import string
log_file = "maclog.txt"


"""
Builds a sendable whatsapp message (self.toLower(message))
"""
def make_message(msg, conversation):
    outgoing_message_enity = TextMessageProtocolEntity(msg, to=conversation)
    return outgoing_message_enity

"""
Logs message to a txt file (maclog.txt, defined above of this class)
"""
def log_mac(message_entity):
    # Nigga who send the message (first name)
    who = message_entity.getNotify().split(" ")[0]

    # Conversation
    conversation = message_entity.getFrom()

    # Message
    message = clean_message(message_entity)

    # Warn
    print("logging something...")

    # Log
    file = open(log_file, "a")
    file.write(
        "------------------------" +
        "\n" + "Sender:" + "\n" + who + "\n" + "Number sender:" + "\n" + conversation +
        "\n" + "Message text:" + "\n" + message + "\n" + "------------------------" + "\n" + "\n")
    file.close()

"""
Cleans all the garbage and non-ASCII characters in the message (idk why whatsapp appends all that garbage)
"""
def clean_message(message_entity):
    message = message_entity.getBody().lower()
    message = message.strip();
    message = ''.join(filter(lambda x: x in string.printable, message))
    return message;

"""
Detects if the message is a command for Mac
"""
def is_command(message):
    macCommand = message[:4]
    return macCommand == "mac,"

"""
Converts a list insto a comma separated string
"""
def nice_list(list):
    return "[" + ", ".join( str(x) for x in list) + "]"