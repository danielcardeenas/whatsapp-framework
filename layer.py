# -*- coding: utf-8 -*-
import time, random, threading, datetime, os

from app.utils import helper
from app.poll import poll
from app.mac import mac

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_contacts.protocolentities import *

from yowsup.layers.protocol_privacy.protocolentities import *
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_profiles.protocolentities import *
from yowsup.common.optionalmodules import PILOptionalModule, AxolotlOptionalModule
from yowsup.layers.protocol_ib.protocolentities import *
from yowsup.layers.protocol_iq.protocolentities import *
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.network import YowNetworkLayer
from yowsup.common import YowConstants
from yowsup.layers.protocol_groups.protocolentities import *


class MacLayer(YowInterfaceLayer):
    PROP_CONTACTS = "org.openwhatsapp.yowsup.prop.syncdemo.contacts"

    def __init__(self):
        super(MacLayer, self).__init__()

    # Callback function when there is a successful connection to Whatsapp server
    # Basic flow. DO NOT TOUCH
    #####################################################################
    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        contacts = self.getProp(self.__class__.PROP_CONTACTS, [])
        print("Sync contacts sucess: " + helper.nice_list(contacts))
        contactEntity = GetSyncIqProtocolEntity(contacts)
        self._sendIq(contactEntity, self.on_sync_result, self.on_sync_error)

    def on_sync_result(self,
                        resultSyncIqProtocolEntity,
                        originalIqProtocolEntity):
        print("Sync result:")
        print(resultSyncIqProtocolEntity)

    def on_sync_error(self,
                       errorSyncIqProtocolEntity,
                       originalIqProtocolEntity):
        print("Sync error:")
        print(errorSyncIqProtocolEntity)

    # Just ignore everything above (this block)
    #####################################################################

    @ProtocolEntityCallback("message")
    def onMessage(self, message_entity):
        print("Type: " + message_entity.getType())
        print("Msg: " + helper.clean_message(message_entity))
        if helper.is_text_message(message_entity):
            # Basic flow. DO NOT TOUCH
            #####################################################################

            # Set received (double v)
            mac.receive_message(self, message_entity)

            # Add message to queue to ACK later
            mac.ack_queue.append(message_entity)

            if mac.should_write(message_entity):
                # Set name Presence
                mac.make_presence(self)

                # Set online
                mac.online(self)
                time.sleep(random.uniform(0.5, 1.5))

                # Set read (double v blue)
                mac.ack_messages(self, message_entity.getFrom())

                # Set is writing
                mac.start_typing(self, message_entity)
                time.sleep(random.uniform(0.5, 2))

                # Set it not writing
                mac.stop_typing(self, message_entity)
                time.sleep(random.uniform(0.3, 0.7))

                # Send the answer, here magic happens
                self.on_text_message(message_entity)
                time.sleep(1)

            # Finally Set offline
            mac.disconnect(self)
            #####################################################################

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print(entity.ack())
        self.toLower(entity.ack())

    def on_text_message(self, message_entity):
        # Log
        helper.log_mac(message_entity)

        # Nigga who send the message (first name only)
        who = message_entity.getNotify().split(" ")[0]

        # Detect command and the predicate of the message
        command = ""
        predicate = ""

        try:
            command = helper.predicate(message_entity).split(' ', 1)[0]
            predicate = helper.predicate(message_entity).split(' ', 1)[1]
        except IndexError:
            print("Could not find predicate")

        if helper.is_command(message_entity):
            handle_message(self, predicate, command, who, message_entity.getFrom())


def handle_message(self, predicate, command, who, conversation):
    if command == "hi" or command == "hola":
        answer = "Hi *" + who + "*"
        mac.send_message(self, answer, conversation)
        print(answer)

    elif command == "help":
        answer = "Hi " + who + "\nNo puedo ayudarte aun"
        mac.send_message(self, answer, conversation)
        print(answer)

    elif command == "siono":
        print("Sending")

    elif command == "poll":
        args = [x.strip() for x in predicate.split(',')]
        _poll = poll.WAPoll(self, args, who)
    else:
        return
