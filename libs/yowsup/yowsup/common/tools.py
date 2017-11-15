import time,datetime,re, hashlib
import calendar
from dateutil import tz
import os
from .constants import YowConstants
import codecs, sys
import logging
import tempfile
import base64
import hashlib
import os.path, mimetypes
from .optionalmodules import PILOptionalModule, FFVideoOptionalModule

# Video
import subprocess
import shlex
import json
import math

logger = logging.getLogger(__name__)

class Jid:
    @staticmethod
    def normalize(number):
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@%s" % (number, YowConstants.WHATSAPP_GROUP_SERVER)
        return "%s@%s" % (number, YowConstants.WHATSAPP_SERVER)

class HexTools:
    decode_hex = codecs.getdecoder("hex_codec")
    @staticmethod
    def decodeHex(hexString):
        result = HexTools.decode_hex(hexString)[0]
        if sys.version_info >= (3,0):
            result = result.decode('latin-1')
        return result

class WATools:
    @staticmethod
    def generateIdentity():
        return os.urandom(20)

    @staticmethod
    def getFileHashForUpload(filePath):
        sha1 = hashlib.sha256()
        f = open(filePath, 'rb')
        try:
            sha1.update(f.read())
        finally:
            f.close()
        b64Hash = base64.b64encode(sha1.digest())
        return b64Hash if type(b64Hash) is str else b64Hash.decode()
    @staticmethod
    def getFileHashForUpload2(filePath):
        sha1 = hashlib.sha256()
        f = open(filePath, 'rb')
        try:
            hash = hashlib.sha256(f.read()).hexdigest()
        finally:
            f.close()
        return hash

class StorageTools:
    @staticmethod
    def constructPath(*path):
        path = os.path.join(*path)
        fullPath = os.path.expanduser(os.path.join(YowConstants.PATH_STORAGE, path))
        if not os.path.exists(os.path.dirname(fullPath)):
            os.makedirs(os.path.dirname(fullPath))
        return fullPath

    @staticmethod
    def getStorageForPhone(phone):
        return StorageTools.constructPath(phone + '/')

    @staticmethod
    def writeIdentity(phone, identity):
        path = StorageTools.getStorageForPhone(phone)
        with open(os.path.join(path, "id"), 'wb') as idFile:
            idFile.write(identity)

    @staticmethod
    def getIdentity(phone):
        path = StorageTools.getStorageForPhone(phone)
        out = None
        idPath = os.path.join(path, "id")
        if os.path.isfile(idPath):
            with open(idPath, 'rb') as idFile:
                out = idFile.read()
        return out

    @staticmethod
    def writeNonce(phone, nonce):
        path = StorageTools.getStorageForPhone(phone)
        with open(os.path.join(path, "nonce"), 'wb') as idFile:
            idFile.write(nonce.encode("latin-1") if sys.version_info >= (3,0) else nonce)

    @staticmethod
    def getNonce(phone):
        path = StorageTools.getStorageForPhone(phone)
        out = None
        noncePath = os.path.join(path, "nonce")
        if os.path.isfile(noncePath):
            with open(noncePath, 'rb') as idFile:
                out = idFile.read()
        return out

class TimeTools:
    @staticmethod
    def parseIso(iso):
        d=datetime.datetime(*map(int, re.split('[^\d]', iso)[:-1]))
        return d

    @staticmethod
    def utcToLocal(dt):
        utc = tz.gettz('UTC')
        local = tz.tzlocal()
        dtUtc =  dt.replace(tzinfo=utc)

        return dtUtc.astimezone(local)

    @staticmethod
    def utcTimestamp():
        utcNow = datetime.datetime.utcnow()
        return calendar.timegm(utcNow.timetuple())

    @staticmethod
    def datetimeToTimestamp(dt):
        return time.mktime(dt.timetuple())

class ImageTools:
    @staticmethod
    def scaleImage(infile, outfile, imageFormat, width, height):
        with PILOptionalModule() as imp:
            Image = imp("Image")
            im = Image.open(infile)
            #Convert P mode images
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail((width, height))
            im.save(outfile, imageFormat)
            return True
        return False

    @staticmethod
    def getImageDimensions(imageFile):
        with PILOptionalModule() as imp:
            Image = imp("Image")
            im = Image.open(imageFile)
            return im.size

    @staticmethod
    def generatePreviewFromImage(image):
        fd, path = tempfile.mkstemp()

        preview = None
        if ImageTools.scaleImage(image, path, "JPEG", YowConstants.PREVIEW_WIDTH, YowConstants.PREVIEW_HEIGHT):
            fileObj = os.fdopen(fd, "rb+")
            fileObj.seek(0)
            preview = fileObj.read()
            fileObj.close()
        os.remove(path)
        return preview

class MimeTools:
    MIME_FILE = os.path.join(os.path.dirname(__file__), 'mime.types')
    mimetypes.init() # Load default mime.types
    try:
        mimetypes.init([MIME_FILE]) # Append whatsapp mime.types
    except Exception as e:
        logger.warning("Unsupported MIME type. System mimes will be used. Cause: " + e.message)

    @staticmethod
    def getMIME(filepath):
        mimeType = mimetypes.guess_type(filepath)[0]
        if mimeType is None:
            raise Exception("Unsupported/unrecognized file type for: "+filepath);
        return mimeType

class VideoTools:
    @staticmethod
    def getVideoProperties(videoFile):
        if sys.version_info <= (3, 0): 
            with FFVideoOptionalModule() as imp:
                VideoStream = imp("VideoStream")
                s = VideoStream(videoFile)
                return s.width, s.height, s.bitrate, s.duration #, s.codec_name
        else:
            return VideoTools.video_meta_data(videoFile)

    @staticmethod
    def generatePreviewFromVideo(videoFile):
        if sys.version_info <= (3, 0):
            with FFVideoOptionalModule() as imp:
                VideoStream = imp("VideoStream")
                fd, path = tempfile.mkstemp('.jpg')
                stream = VideoStream(videoFile)
                stream.get_frame_at_sec(0).image().save(path)
                preview = ImageTools.generatePreviewFromImage(path)
                os.remove(path)
                return preview
        else:
            import moviepy.editor as mvpy
            
            clip = mvpy.VideoFileClip(videoFile)
            path = tempfile.mkstemp('.jpg')[1]
            clip.save_frame(path)
            preview = ImageTools.generatePreviewFromImage(path)
            os.remove(path)
            return preview

    @staticmethod
    def video_meta_data(path):
        cmd = "ffprobe -v quiet -print_format json -show_streams"
        args = shlex.split(cmd)
        args.append(path)
        
        # run the ffprobe process, decode stdout into utf-8 & convert to JSON
        ffprobeOutput = subprocess.check_output(args).decode('utf-8')
        ffprobeOutput = json.loads(ffprobeOutput)
    
        height = ffprobeOutput['streams'][0]['height']
        width = ffprobeOutput['streams'][0]['width']
        bit_rate = ffprobeOutput['streams'][0]['bit_rate']
        duration = ffprobeOutput['streams'][0]['duration']
        
        #print(height, width, br, duration)
        return width, height, int(float(bit_rate)), int(math.ceil(float(duration)))
