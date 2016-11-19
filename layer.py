# -*- coding: utf-8 -*-
import time
import random

from app.utils import helper
from app.poll import poll
from app.mac import mac
from app.yesno.yesno import YesNo
from app.receiver import receiver

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_contacts.protocolentities import *

from yowsup.layers.protocol_groups.protocolentities import *

'''
Basic flow. DO NOT TOUCH
Modifying this block automatically makes you a piece of shit
####################################################################################################################
####################################################################################################################
'''
class MacLayer(YowInterfaceLayer):
    PROP_CONTACTS = "org.openwhatsapp.yowsup.prop.syncdemo.contacts"

    def __init__(self):
        super(MacLayer, self).__init__()

    # Callback function when there is a successful connection to Whatsapp server
    @ProtocolEntityCallback("success")
    def onSuccess(self, success_entity):
        contacts = self.getProp(self.__class__.PROP_CONTACTS, [])
        print("Sync contacts sucess: " + helper.nice_list(contacts))
        contact_entity = GetSyncIqProtocolEntity(contacts)
        self._sendIq(contact_entity, self.on_sync_result, self.on_sync_error)

    def on_sync_result(self,
                       result_sync_iq_entity,
                       original_iq_entity):
        print("Sync result:")
        print(result_sync_iq_entity)

    def on_sync_error(self,
                      error_sync_iq_entity,
                      original_iq_entity):
        print("Sync error:")
        print(error_sync_iq_entity)


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
        #print(entity.ack())


    @ProtocolEntityCallback("message")
    def onMessage(self, message_entity):
        if helper.is_text_message(message_entity):

            # Set received (double v) and add to ack queue
            mac.receive_message(self, message_entity)

            # Handle intercepts if needed
            receiver.handle_intercepts(self, message_entity)

            # If is a mac order. (Message starts with '!')
            if mac.should_write(message_entity):
                # Prepare mac to answer (Human behavior)
                mac.prepate_answer(self, message_entity)

                # Send the answer, here magic happens
                self.on_text_message(message_entity)
                time.sleep(random.uniform(0.5, 1.5))

            # Finally Set offline
            mac.disconnect(self)

    def on_text_message(self, message_entity):
        # Detect command and the predicate of the message
        command = ""
        predicate = ""

        try:
            command = helper.predicate(message_entity).split(' ', 1)[0]
            predicate = helper.predicate(message_entity).split(' ', 1)[1]
        except IndexError:
            print("No predicate")

        # Log
        # helper.log_mac(message_entity)

        if helper.is_command(message_entity):
            handle_message(self, predicate, command, message_entity, message_entity.getFrom())

'''
Just ignore everything above (this block)
Modifying this block automatically makes you a piece of shit
####################################################################################################################
####################################################################################################################
'''


# You can touch code below here this line (:
####################################################################################################################

'''
This method gets all you need in a command message.
For ex.
    In group "ITS", daniel sent "!hola a todos"
    @self = the MacLayer (You need this to send reply with mac -> mac.send_message())
    @command = What comes after '!'. In this case "hola"
    @predicate = What comes after command. In this case "a todos"
    @who = Who sent this. In this case daniel (check below for retrieving the name)
    @conversation = The jId of the conversation. In this case the group "ITS".
                    NOTE: You can only send messages to conversations
'''
def handle_message(self, command, predicate, message_entity, conversation):
    # Nigga who send the message (first name)
    who = message_entity.getNotify().split(" ")[0]

    if command == "hi" or command == "hola":
        answer = "Hola *" + who + "*"
        mac.send_message(self, answer, conversation)
        print(answer)

    elif command == "help":
        answer = "Hola *" + who + "*\nNo puedo ayudarte por ahora"
        mac.send_message(self, answer, conversation)
        print(answer)

    elif command == "siono":
        yesno = YesNo(self, conversation)
        yesno.send_yesno()

    elif command == "poll":
        args = [x.strip() for x in predicate.split(',')]
        _poll = poll.WAPoll(self, args, who)
    else:
        return
