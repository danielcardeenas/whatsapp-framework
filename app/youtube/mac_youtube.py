import os
from urllib.parse import urlparse
from app.receiver.receiver import Receiver
from app.utils import helper
from app.mac import mac
from pytube import YouTube


class WAYoutube(Receiver):
    def __init__(self, instance, creator, conversation, identifier="__global__"):
        Receiver.__init__(self, identifier, creator, self.handle_answer)
        self.instance = instance
        self.creator = creator
        self.conversation = conversation

    def handle_answer(self, message_entity=None):
        message = helper.clean_message(message_entity)
        if is_youtube_url(message):
            yt = YouTube(message)
            video = get_default_video(yt)

            path = "app/assets/videos/" + yt.filename + ".mp4"
            if os.path.exists(path):
                os.remove(path)

            video.download('app/assets/videos')
            mac.send_video(self.instance, self.conversation, path, caption="video")


def is_youtube_url(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return True
    elif query.hostname in ('www.youtube.com', 'youtube.com'):
        return True
    else:
        return False


def get_default_video(yt, preferred='mp4'):
    """
    Return the highest quality resolution available that matches the
    preferred filetype, if available. Will favour the highest quality
    over the preferred filetype. If not available, the highest
    quality that matches any filetype is returned.
    Keyword arguments:
    preferred -- the preferred extension (e.g.: mp4)
    """
    highest, result = 0, None
    for v in yt.videos:
        current = int(v.resolution[0])
        if ((current > highest) or
                (current == highest and v.extension == preferred)):
            highest = current
            result = v

    return result
