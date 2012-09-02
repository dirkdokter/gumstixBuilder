import os, errno
from tarfile import TarFile 

def createFolderIfNotExist(path):
    try:
        os.makedirs(path)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

class NewTarFile(TarFile):
    def extract(self, member, path="", strip=0):
        """Extract a member from the archive to the current working directory,
           using its full name. Its file information is extracted as accurately
           as possible. `member' may be a filename or a TarInfo object. You can
           specify a different directory using `path'.
        """
        self._check("r")

        if isinstance(member, basestring):
            tarinfo = self.getmember(member)
        else:
            tarinfo = member

        # Prepare the link target for makelink().
        if tarinfo.islnk():
            tarinfo._link_target = os.path.join(path, tarinfo.linkname)

        try:
            self._extract_member(tarinfo, os.path.join(path, tarinfo.name))
        except EnvironmentError, e:
            if self.errorlevel > 0:
                raise
            else:
                if e.filename is None:
                    self._dbg(1, "tarfile: %s" % e.strerror)
                else:
                    self._dbg(1, "tarfile: %s %r" % (e.strerror, e.filename))
        except ExtractError, e:
            if self.errorlevel > 1:
                raise
            else:
                self._dbg(1, "tarfile: %s" % e)
                
