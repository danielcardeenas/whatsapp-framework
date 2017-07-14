# -*- coding utf-8 -*-
import time
import random

from app.utils import helper
from app.mac import mac, signals
from app.receiver import receiver
from app.models.message import Message

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_contacts.protocolentities import *

from yowsup.layers.protocol_groups.protocolentities import *

'''
Basic flow. DO NOT TOUCH
Modifying this block automatically makes you a piece of shit
################################################################################
################################################################################
'''
class MacLayer(YowInterfaceLayer):
    PROP_CONTACTS = "org.openwhatsapp.yowsup.prop.syncdemo.contacts"

    def __init__(self):
        super(MacLayer, self).__init__()
        signals.initialized.send(self)

    # Callback function when there is a successful connection to Whatsapp server
    @ProtocolEntityCallback("success")
    def on_success(self, success_entity):
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
    def on_receipt(self, entity):
        self.toLower(entity.ack())


    @ProtocolEntityCallback("message")
    def on_message(self, message_entity):
        if helper.is_text_message(message_entity):
            mac.set_entity(self)

            # Set received (double v) and add to ack queue
            mac.receive_message(self, message_entity)

            # Handle intercepts if needed}
            # Not needed anymore
            #receiver.intercept(self, message_entity)
            
            # Send signal
            self.send_message_signal(message_entity)

            # Finally set offline
            mac.disconnect(self)
            
    def send_message_signal(self, message_entity):
        #helper.log_mac(message_entity) # Log the messages into txt file
        signals.message_received.send(Message(message_entity))

'''
Just ignore everything above (this block)
Modifying this block automatically makes you a piece of shit
################################################################################
################################################################################
'''