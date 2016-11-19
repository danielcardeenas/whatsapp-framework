# -*- coding: utf-8 -*-
import time, random, datetime, os

from app.utils import helper
from app.poll import poll

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_presence.protocolentities import *
from yowsup.layers.protocol_contacts.protocolentities import *
from yowsup.layers.protocol_chatstate.protocolentities import *
from yowsup.common.tools import Jid

from yowsup.layers.protocol_privacy.protocolentities import *
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_profiles.protocolentities import *
from yowsup.common.optionalmodules import PILOptionalModule, AxolotlOptionalModule
from yowsup.layers.protocol_messages.protocolentities import *
from yowsup.layers.protocol_ib.protocolentities import *
from yowsup.layers.protocol_iq.protocolentities import *
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.network import YowNetworkLayer
from yowsup.common import YowConstants
from yowsup.layers.protocol_groups.protocolentities import *

name = "MacPresence"


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
        print(resultSyncIqProtocolEntity)

    def on_sync_error(self,
                       errorSyncIqProtocolEntity,
                       originalIqProtocolEntity):
        print(errorSyncIqProtocolEntity)

    # Just ignore
    #####################################################################


    @ProtocolEntityCallback("message")
    def onMessage(self, message_entity):
        if message_entity.getType() == 'text':
            # Basic flow. DO NOT TOUCH
            #####################################################################
            # Set received (double v)
            self.toLower(message_entity.ack())
            time.sleep(random.uniform(0.5, 2))

            # Set name Presence
            self.toLower(PresenceProtocolEntity(name=name))

            # Set online
            self.toLower(AvailablePresenceProtocolEntity())
            time.sleep(random.uniform(0.5, 1.5))

            # Set read (double v blue)
            self.toLower(message_entity.ack(True))

            if shouldWrite(message_entity):
                time.sleep(random.uniform(0.5, 1.5))

                # Set is writing
                self.toLower(OutgoingChatstateProtocolEntity(
                    OutgoingChatstateProtocolEntity.STATE_TYPING,
                    Jid.normalize(message_entity.getFrom(False))
                ))
                time.sleep(1)

                # Set it not writing
                self.toLower(OutgoingChatstateProtocolEntity(
                    OutgoingChatstateProtocolEntity.STATE_PAUSED,
                    Jid.normalize(message_entity.getFrom(False))
                ))
                time.sleep(1)

                # Send the answer, here magic happens
                self.onTextMessage(message_entity)
                time.sleep(3)

            # Finally Set offline
            self.toLower(UnavailablePresenceProtocolEntity())
            #####################################################################

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print(entity.ack())
        self.toLower(entity.ack())

    def onTextMessage(self, message_entity):
        # Nigga who send the message (first name)
        who = message_entity.getNotify().split(" ")[0]

        # Message
        message = helper.clean_message(message_entity)

        # Conversation
        conversation = message_entity.getFrom()

        # Log (duh!)
        # logMac(message_entity)

        if (helper.is_command(message)):
            handleMessage(self, message_entity, message[4:].strip(), who, conversation);


def shouldWrite(message_entity):
    return helper.is_command(helper.clean_message(message_entity))


def handleMessage(self, message_entity, message, who, conversation):
    if message == "hi" or message == "hola":
        answer = "Hi *" + who + "*"
        self.toLower(helper.make_message(answer, message_entity.getFrom()))
        print(answer)

    elif message == "help":
        answer = "Hi " + who + "\nNo puedo ayudarte negro"
        self.toLower(helper.make_message(answer, message_entity.getFrom()))
        print(answer)

    elif message == "poll":
        _poll = poll.WAPoll(self, "Nueva poll", message_entity.getFrom())
        _poll.sendPoll()

    else:
        helper.log_mac(message_entity)