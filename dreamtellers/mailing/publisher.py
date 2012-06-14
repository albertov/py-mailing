from cStringIO import StringIO

from ftputil import FTPHost

class FTPPublisher(object):
    FTPHost = FTPHost  # for mock inyection in tests
    def __init__(self, composer):
        self._composer = composer

    def publish(self, host, username, password, dir='/'):
        with self.FTPHost(host, username, password) as ftp:
            dir = dir.rstrip('/') + '/'
            ftp.makedirs(dir)
            for fname, data in self._composer.files:
                dest = ftp.file(dir+fname, 'w')
                ftp.copyfileobj(StringIO(data), dest)
                dest.close()