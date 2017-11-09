import sys, tempfile, logging, os
logger = logging.getLogger(__name__)

if sys.version_info >= (3, 0):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode


class MediaDownloader:
    def __init__(self, successClbk = None, errorClbk = None, progressCallback = None):
        self.successCallback = successClbk
        self.errorCallback = errorClbk
        self.progressCallback = progressCallback

    def download(self, url="", path=""):
        try:
            u = urlopen(url)

            if path == "":
                path = "app/assets/received/" + tempfile.mkstemp()[1].rsplit('/', 1)[-1]
                
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                meta = u.info()

                if sys.version_info >= (3, 0):
                    fileSize = int(u.getheader("Content-Length"))
                else:
                    fileSize = int(meta.getheaders("Content-Length")[0])

                fileSizeDl = 0
                blockSz = 8192
                lastEmit = 0
                while True:
                    buf = u.read(blockSz)

                    if not buf:
                        break

                    fileSizeDl += len(buf)
                    f.write(buf)
                    status = (fileSizeDl * 100 / fileSize)

                    if self.progressCallback and lastEmit != status:
                        self.progressCallback(int(status))
                        lastEmit = status;

            if self.successCallback:
                self.successCallback(path)
                
            return path;
        except:
            logger.exception("Error occured at transfer")
            if self.errorCallback:
                self.errorCallback();