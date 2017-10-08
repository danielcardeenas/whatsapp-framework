# -*- coding: utf-8 -*-

from yowsup.layers.protocol_messages.protocolentities import *
import string
from pprint import pprint

log_file = "maclog.txt"
me = "5218114140740@s.whatsapp.net" # Daniel Cardenas

def get_who_send(message_entity):
    who = message_entity.getFrom()
    if message_entity.isGroupMessage():
        who = message_entity.getParticipant()
        
    return who
    
    
def sender_name(message_entity):
    name = message_entity.getNotify()
    name = name.encode('latin-1')
    name = name.decode('utf-8')
    return name


def get_conversation(message_entity):
    return message_entity.getFrom()

"""
Detects if the message entity is text type.
"""
def is_text_message(message_entity):
    return message_entity.getType() == "text"

"""
Detects if the message entity is media type.
Available media types:
    + image
    + audio i guess
    + location
    + vcard
"""
def is_media_message(message_entity):
    return message_entity.getType() == "media"


"""
Detects if the message entity is media -> image type
"""
def is_image_media(message_entity):
    if is_media_message(message_entity):
        return message_entity.getMediaType() == "image"


"""
Detects if the message entity is media -> image type
"""
def is_location_media(message_entity):
    if is_media_message(message_entity):
        return message_entity.getMediaType() == "location"


"""
Detects if the message entity is media -> image type
"""
def is_vcard_media(message_entity):
    if is_media_message(message_entity):
        return message_entity.getMediaType() == "vcard"


"""
Builds a sendable text whatsapp message (self.toLower(message))
"""
def make_message(msg, conversation):
    outgoing_message_enity = TextMessageProtocolEntity(msg, to=conversation)
    return outgoing_message_enity


"""
Logs message to a txt file (maclog.txt, defined above of this class)
"""
def log_txt(message_entity):
    # Nigga who send the message (first name)
    who = who = sender_name(message_entity)

    # Conversation
    conversation = message_entity.getFrom()

    # Message
    message = message_entity.getBody()
    message = message.strip()
    message = ''.join(filter(lambda x: x in string.printable, message))
    message = message.strip()
    
    dirty = message_entity.getBody().strip()

    # Warn
    print("logging something...")

    # Log
    file = open(log_file, "a")
    file.write(
        "------------------------" +
        "\n" + "Sender:" + "\n" + who + "\n" + "Number sender:" + "\n" + conversation +
        "\n" + "Real msg:" + "\n" + dirty + "\n" +
        "\n" + "Clean msg:" + "\n" + message + "\n" +
        "------------------------" + "\n" + "\n")
    file.close()
    

"""
Deep print
"""
def log(message_entity):
    pprint(vars(message_entity))
    

"""
Returns predicate of the message
"""
def message(message):
    message = clean_message(message)
    if is_command(message):
        return message[1:]
    else:
        return message


"""
Cleans all the garbage and non-ASCII characters in the message (idk why whatsapp appends all that garbage)
"""
def clean_message(message_entity):
    message = message_entity.getBody()
    message = message.strip()
    #message = ''.join(filter(lambda x: x in string.printable, message))
    return message


"""
Detects if the message is a command for Mac
"""
def is_command(message):
    macShorcut = message[:1]
    return macShorcut == "!"


"""
Converts a list into a comma separated string
"""
def nice_list(list):
    return "[" + ", ".join( str(x) for x in list) + "]"
    

"""
Retrieves the command from the message.
command is what goes after the '!'
"""
def command(message_entity):
    command = ""
    try:
        command = message(message_entity).split(' ', 1)[0]
    except IndexError:
        print("Command error")
    
    return command
    
    
"""
Retrieves the predicate from the message.
predicate is what goes after the command
"""     
def predicate(message_entity):
    rest = ""
    try:
        rest = message(message_entity).split(' ', 1)[1]
    except IndexError:
        pass
    
    return rest
    