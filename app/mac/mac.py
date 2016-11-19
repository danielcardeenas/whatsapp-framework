import os.path
import logging
import sys
from yowsup.layers.protocol_presence.protocolentities import *
from yowsup.layers.protocol_chatstate.protocolentities import *
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.common.tools import Jid

from app.utils import helper

name = "MacPresence"
ack_queue = []
logger = logging.getLogger(__name__)

def receive_message(self, message_entity):
    self.toLower(message_entity.ack())


def make_presence(self):
    self.toLower(PresenceProtocolEntity(name=name))


def online(self):
    self.toLower(AvailablePresenceProtocolEntity())


def disconnect(self):
    self.toLower(UnavailablePresenceProtocolEntity())


def start_typing(self, message_entity):
    self.toLower(OutgoingChatstateProtocolEntity(
        OutgoingChatstateProtocolEntity.STATE_TYPING,
        Jid.normalize(message_entity.getFrom(False))
    ))


def stop_typing(self, message_entity):
    self.toLower(OutgoingChatstateProtocolEntity(
        OutgoingChatstateProtocolEntity.STATE_PAUSED,
        Jid.normalize(message_entity.getFrom(False))
    ))


def should_write(message_entity):
    return helper.is_command(message_entity)


def ack_messages(self, conversation):
    # Filter messages from this conversation
    queue = [message_entity for message_entity in ack_queue if same_conversation(message_entity, conversation)]

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


def send_message(self, message, conversation):
    self.toLower(helper.make_message(message, conversation))


def send_image(self, number, path, caption=None):
    if os.path.isfile(path):
        media_send(self, number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, caption)
    else:
        print("Image doesn't exists")


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
def on_request_upload_result(self, jid, mediaType, filePath, resultRequestUploadIqProtocolEntity,
                             requestUploadIqProtocolEntity, caption = None):
    if resultRequestUploadIqProtocolEntity.isDuplicate():
        doSendMedia(self, mediaType, filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                         resultRequestUploadIqProtocolEntity.getIp(), caption)
    else:
        successFn = lambda filePath, jid, url: doSendMedia(self,
                                                           mediaType,
                                                           filePath,
                                                           url,
                                                           jid,
                                                           resultRequestUploadIqProtocolEntity.getIp(),
                                                           caption)
        mediaUploader = MediaUploader(jid,
                                      self.getOwnJid(),
                                      filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn,
                                      onUploadError(self,
                                                    filePath,
                                                    jid),
                                      onUploadProgress(self,
                                                       filePath,
                                                       jid,
                                                       resultRequestUploadIqProtocolEntity.getResumeOffset()),
                                      async=False)
        mediaUploader.start()


def on_request_upload_error(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
    logger.error("Request upload for file %s for %s failed" % (path, jid))


def doSendMedia(self, mediaType, filePath, url, to, ip=None, caption=None):
    if mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE:
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption=caption)
    elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
        entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
    elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO:
        entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption=caption)
    self.toLower(entity)


def onUploadError(self, filePath, jid):
    logger.error("Upload file %s to %s failed!" % (filePath, jid))


def onUploadProgress(self, filePath, jid, progress):
    sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
    sys.stdout.flush()

