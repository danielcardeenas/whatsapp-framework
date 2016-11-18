# -*- coding: utf-8 -*-
import time, string, datetime, os

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.network import YowNetworkLayer
from yowsup.common import YowConstants
from yowsup.layers.protocol_groups.protocolentities import *
from yowsup.layers.protocol_presence.protocolentities import *
from yowsup.layers.protocol_messages.protocolentities import *
from yowsup.layers.protocol_ib.protocolentities import *
from yowsup.layers.protocol_iq.protocolentities import *
from yowsup.layers.protocol_contacts.protocolentities import *
from yowsup.layers.protocol_chatstate.protocolentities import *
from yowsup.layers.protocol_privacy.protocolentities import *
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_profiles.protocolentities import *
from yowsup.common.tools import Jid
from yowsup.common.optionalmodules import PILOptionalModule, AxolotlOptionalModule

name = "MacPresence"
filelog = "maclog.txt"


class MacLayer(YowInterfaceLayer):
    PROP_CONTACTS = "org.openwhatsapp.yowsup.prop.syncdemo.contacts"

    def __init__(self):
        super(MacLayer, self).__init__()

    # Callback function when there is a successful connection to Whatsapp server
    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        contacts = self.getProp(self.__class__.PROP_CONTACTS, [])
        print("Sync contacts sucess: " + getNiceList(contacts))
        contactEntity = GetSyncIqProtocolEntity(contacts)
        self._sendIq(contactEntity, self.onGetSyncResult, self.onGetSyncError)

    def onGetSyncResult(self, resultSyncIqProtocolEntity, originalIqProtocolEntity):
        print(resultSyncIqProtocolEntity)
        #raise KeyboardInterrupt()

    def onGetSyncError(self, errorSyncIqProtocolEntity, originalIqProtocolEntity):
        print(errorSyncIqProtocolEntity)
        #raise KeyboardInterrupt()


    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            # Basic flow. DO NOT TOUCH
            #####################################################################
            time.sleep(0.5)

            # Set received (double v)
            self.toLower(messageProtocolEntity.ack())
            time.sleep(0.5)

            # Set name Presence
            self.toLower(PresenceProtocolEntity(name=name))
            time.sleep(0.5)

            # Set online
            self.toLower(AvailablePresenceProtocolEntity())
            time.sleep(0.5)

            # Set read (double v blue)
            self.toLower(messageProtocolEntity.ack(True))
            time.sleep(0.5)

            if shouldWrite(messageProtocolEntity):
                # Set is writing
                self.toLower(OutgoingChatstateProtocolEntity(
                    OutgoingChatstateProtocolEntity.STATE_TYPING,
                    Jid.normalize(messageProtocolEntity.getFrom(False))
                ))
                time.sleep(1)

                # Set it not writing
                self.toLower(OutgoingChatstateProtocolEntity(
                    OutgoingChatstateProtocolEntity.STATE_PAUSED,
                    Jid.normalize(messageProtocolEntity.getFrom(False))
                ))
                time.sleep(1)

                # Send the answer, here magic happens
                self.onTextMessage(messageProtocolEntity)
                time.sleep(3)

            # Finally Set offline
            self.toLower(UnavailablePresenceProtocolEntity())
            #####################################################################

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print(entity.ack())
        self.toLower(entity.ack())

    def onTextMessage(self, messageProtocolEntity):
        # Nigga who send the message (first name)
        who = messageProtocolEntity.getNotify().split(" ")[0]

        # Message
        message = getCleanMessage(messageProtocolEntity)

        # Conversation
        conversation = messageProtocolEntity.getFrom()

        # Log (duh!)
        # logMac(messageProtocolEntity)

        if (isCommand(message)):
            handleMessage(self, messageProtocolEntity, message[4:].strip(), who, conversation);


def makeMessage(message, recipient):
    outgoingMessageProtocolEntity = TextMessageProtocolEntity(message, to=recipient)
    return outgoingMessageProtocolEntity


def isCommand(message):
    macCommand = message[:4]
    return macCommand == "mac,"


def shouldWrite(messageProtocolEntity):
    return isCommand(getCleanMessage(messageProtocolEntity))


def getCleanMessage(messageProtocolEntity):
    message = messageProtocolEntity.getBody().lower()
    message = message.strip();
    message = ''.join(filter(lambda x: x in string.printable, message))
    return message;


def handleMessage(self, messageProtocolEntity, message, who, conversation):
    if message == "hi" or message == "hola":
        answer = "_Hi_ " + who + " "
        self.toLower(makeMessage(answer, messageProtocolEntity.getFrom()))
        print(answer)

    elif message == "help":
        answer = "Hi " + who + "\n\nNo puedo ayudarte negro"
        self.toLower(makeMessage(answer, messageProtocolEntity.getFrom()))
        print(answer)

    else:
        logMac(messageProtocolEntity)


def logMac(messageProtocolEntity):
    # Nigga who send the message (first name)
    who = messageProtocolEntity.getNotify().split(" ")[0]

    # Conversation
    conversation = messageProtocolEntity.getFrom()

    # Message
    message = getCleanMessage(messageProtocolEntity)

    # Warn
    print("logging something...")

    # Log
    outFile = open(filelog, "a")
    outFile.write(
        "------------------------" +
        "\n" + "Sender:" + "\n" + who + "\n" + "Number sender:" + "\n" + conversation +
        "\n" + "Message text:" + "\n" + message + "\n" + "------------------------" + "\n" + "\n")
    outFile.close()

def getNiceList(list):
    return "[" + ", ".join( str(x) for x in list) + "]"