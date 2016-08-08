"""
外观模式
将较为复杂的接口简单化
"""

import zipfile
import gzip
import tarfile
import string
import os
import re


class Archive:
    def __init__(self, filename):
        self._names = None
        self._unpack = None
        self._file = None
        self.filename = filename

    @property
    def filename(self):
        return self.__filename

    @property.setter
    def filename(self, name):
        self.close()
        self.__filename = name

    def close(self):
        if self._file is not None:
            self._file.close()
        self._names = self._unpack = self._file = None

    def names(self):
        if self._file is None:
            self._prepare()
        return self._names()

    def unpack(self):
        if self._file is None:
            self._prepare()
        self._unpack()

    def _prepare(self):
        if self.filename.endswith((".tar.gz", ".tar.bz2", ".tar.xz", ".zip")):
            self._prepare_tarball_or_zip()
        elif self.filename.endswith(".gz"):
            self._prepare_gzip()
        else:
            raise ValueError("unreadable: {}".format(self.filename))

    def _prepare_tarball_or_zip(self):
        def safe_extractall():
            unsafe = []
            for name in self.names():
                if not self.is_safe(name):
                    unsafe.append(name)
                if unsafe:
                    raise ValueError("unsafe to unpack: {}".format(unsafe))
                self._file.extractall()
        if self.filename.endswith(".zip"):
            self._file = zipfile.ZipFile(self.filename)
            self._names = self._file.namelist
            self._unpack = safe_extractall
        else:
            suffix = os.path.splitext(self.filename)[1]
            self._file = tarfile.open(self.filename, "r:" + suffix[1:])
            self._names = self._file.getnames
            self._unpack = safe_extractall

    def prepare_gzip(self):
        self._file = gzip.open(self.filename)
        filename = self.filename[:-3]
        self._names = lambda: [filename]
        def extractall():
            with open(filename, "wb") as file:
                file.write(self._file.read())
        self._upack = extractall()

    def is_safe(self, filename):
        return not (filename.startswith("/", "\\")) or \
        (len(filename) > 1 and filename[1] == ":" and filename[0] in
         string.ascii_letter) or re.search(r"[.][.][/\\]", filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __str__(self):
        return "{}({})".format(self.filename, self._file is not None)


if __name__ == '__main__':
    import errno
    import os
    import shutil
    import tempfile
    fromPath = os.path.dirname(os.path.abspath(__file__))
    toPath = os.path.join(tempfile.gettempdir(), "unpack")
    try:
        os.makedirs(toPath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    zipFilename = os.path.join(toPath, "test.zip")
    zipNames = ["decorator1.py", "decorator2.py", "render1.py"]
    tarFilename = os.path.join(toPath, "test.tar.gz")
    tarNames = ["stationery1.py", "stationery2.py"]
    gzFilename = os.path.join(toPath, "hello.pyw.gz")
    gzName = "hello.pyw"
    file = None
    try:
        file = zipfile.ZipFile(zipFilename, "w", zipfile.ZIP_DEFLATED)
        for name in zipNames:
            file.write(name)
    finally:
        if file is not None:
            file.close()
    file = None
    try:
        file = tarfile.open(tarFilename, "w:gz")
        for name in tarNames:
            file.add(name)
    finally:
        if file is not None:
            file.close()
    file = None
    try:
        file = gzip.open(gzFilename, "w")
        with open(gzName, "rb") as infile:
            file.write(infile.read())
    finally:
        if file is not None:
            file.close()

    os.chdir(toPath)
    with Archive(zipFilename) as archive:
        print(archive.names())
        assert archive.names() == zipNames
        archive.unpack()

        archive.filename = tarFilename
        print(archive.names())
        assert archive.names() == tarNames
        archive.unpack()

        archive.filename = gzFilename
        archive.unpack()

    shutil.rmtree(toPath)
