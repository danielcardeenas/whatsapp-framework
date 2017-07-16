# -*- coding: utf-8 -*-

import os.path
import logging
import sys
import time
import random
import string
from yowsup.layers.protocol_presence.protocolentities import *
from yowsup.layers.protocol_chatstate.protocolentities import *
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.common.tools import Jid

from app.utils import helper

# Globar entity
entity = None

name = "Mac"
ack_queue = []
commands = [ 
    "hi",
    "poll",
    "yt",
    "help",
    "siono",
    "poll2",
    "elo"
]
logger = logging.getLogger(__name__)

def set_entity(instance):
    global entity
    entity = instance


def receive_message(self, message_entity):
    self.toLower(message_entity.ack())
    # Add message to queue to ACK later
    ack_queue.append(message_entity)


def prepate_answer(self, conversation):
    # Set name Presence
    make_presence(self)

    # Set online
    online(self)
    time.sleep(random.uniform(0.5, 1.5))

    # Set read (double v blue)
    ack_messages(self, conversation)

    # Set is writing
    start_typing(self, conversation)
    time.sleep(random.uniform(0.5, 2))

    # Set it not writing
    stop_typing(self, conversation)
    time.sleep(random.uniform(0.3, 0.7))


def make_presence(self):
    self.toLower(PresenceProtocolEntity(name=name))


def online(self):
    self.toLower(AvailablePresenceProtocolEntity())


def disconnect(self):
    self.toLower(UnavailablePresenceProtocolEntity())


def start_typing(self, conversation):
    self.toLower(OutgoingChatstateProtocolEntity(
        OutgoingChatstateProtocolEntity.STATE_TYPING,
        Jid.normalize(conversation)
    ))


def stop_typing(self, conversation):
    self.toLower(OutgoingChatstateProtocolEntity(
        OutgoingChatstateProtocolEntity.STATE_PAUSED,
        Jid.normalize(conversation)
    ))


def is_in_command_list(message_entity):
    try:
        command = helper.predicate(message_entity).split(' ', 1)[0]
        if command in commands:
            return True
    except:
        return False
        
    return False


def ack_messages(self, conversation):
    # Filter messages from this conversation
    queue = [message_entity for message_entity in ack_queue if same_conversation(message_entity, conversation)]

    # Get only last 20 messages (Will discard reading the others)
    queue = queue[-20:]

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


def send_message(str_message, conversation):
    message = decode_string(str_message)
    
    # Prepare mac to answer (Human behavior)
    prepate_answer(entity, conversation)
    entity.toLower(helper.make_message(message, conversation))
    
    
def send_image(conversation, path, caption=None):
    if os.path.isfile(path):
        media_send(entity, conversation, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, caption)
    else:
        print("Image doesn't exists")


def decode_string(message):
    try:
        if type(message) is bytes:
            message = message.decode(encoding='latin1', errors='ignore')
        return message
    except:
        return message.decode('utf-8','ignore').encode("utf-8")


def send_video(self, number, path, caption=None):
    if os.path.isfile(path):
        media_send(self, number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO)
    else:
        print("Video doesn't exists")


def media_send(self, number, path, media_type, caption=None):
    jid = number
    entity = RequestUploadIqProtocolEntity(media_type, filePath=path)
    fn_success = lambda success_entity, original_entity: on_request_upload_result(self, jid, media_type, path,
                                                                                    success_entity, original_entity,
                                                                                    caption)
    fn_error = lambda error_entity, original_entity: on_request_upload_error(self, jid, path, error_entity, original_entity)
    self._sendIq(entity, fn_success, fn_error)


'''
Callbacks. Do not touch
'''
def on_request_upload_result(self, jid, media_type, file_path, result_request_upload_entity,
                             request_upload_entity, caption=None):
    if result_request_upload_entity.isDuplicate():
        do_send_media(self, media_type, file_path, result_request_upload_entity.getUrl(), jid,
                      result_request_upload_entity.getIp(), caption)
    else:
        success_fn = lambda file_path, jid, url: do_send_media(self,
                                                               media_type,
                                                               file_path,
                                                               url,
                                                               jid,
                                                               result_request_upload_entity.getIp(),
                                                               caption)
        media_uploader = MediaUploader(jid,
                                       self.getOwnJid(),
                                       file_path,
                                       result_request_upload_entity.getUrl(),
                                       result_request_upload_entity.getResumeOffset(),
                                       success_fn,
                                       on_upload_error(self, file_path, jid),
                                       on_upload_progress(self,
                                                          file_path,
                                                          jid,
                                                          result_request_upload_entity.getResumeOffset()),
                                       async=False)
        media_uploader.start()


def on_request_upload_error(self, jid, path, error_request_upload_iq_entity, request_upload_iq_entity):
    logger.error("Request upload for file %s for %s failed" % (path, jid))


def do_send_media(self, media_type, file_path, url, to, ip=None, caption=None):
    if media_type == RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE:
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to, caption=caption)
        self.toLower(entity)
    elif media_type == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
        entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to)
        self.toLower(entity)
    elif media_type == RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO:
        entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to, caption=caption)
        self.toLower(entity)


def on_upload_error(self, filePath, jid):
    logger.error("Upload file %s to %s failed!" % (filePath, jid))


def on_upload_progress(self, filePath, jid, progress):
    sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
    sys.stdout.flush()

