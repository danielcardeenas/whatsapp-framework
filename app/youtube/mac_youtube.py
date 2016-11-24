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
            try:
                yt = YouTube(message)
                video = yt.get('mp4')
                video.download('app/assets/videos')
                path = "app/assets/videos/" + yt.filename + ".mp4"
                mac.send_video(self.instance, self.conversation, path, caption="video")
            except:
                print("Could send video")


def is_youtube_url(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return True
    elif query.hostname in ('www.youtube.com', 'youtube.com'):
        return True
    else:
        return False