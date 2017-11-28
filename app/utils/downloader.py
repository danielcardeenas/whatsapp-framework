import os

from yowsup.layers.protocol_media.mediadownloader import MediaDownloader
from app.utils import helper
from app.utils import media_decrypter
from pprint import pprint

"""
Downloads & Decrypts
Returns file path of the message attached in the message
"""
def get_file(message_entity):
    enc_path = download_enc(message_entity)
    out_file = decrypt_file(message_entity, enc_path)
    
    # Remove enc file
    try:
        os.remove(enc_path)
    except OSError:
        pass
    
    return out_file
    

"""
Downloads enc from url from message_entity and returns its path
"""
def download_enc(message_entity):
    url = message_entity.getMediaUrl()
    return MediaDownloader().download(url.decode('ASCII'))
    
    
"""
Decrypts enc file and returns its path
"""
def decrypt_file(message_entity, enc_path):
    pprint(vars(message_entity))
    key = message_entity.getMediaKey()
    type = message_entity.getMediaType()
    out = ""
    
    if helper.is_image_media(message_entity):
        out = os.path.splitext(enc_path)[0] + '.jpg'
    
    return media_decrypter.decrypt_file(enc_path, key, type, out)