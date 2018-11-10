import os
from io import BlockingIOError

from spinn_storage_handlers.abstract_classes \
    import AbstractBufferedDataStorage, AbstractContextManager
from spinn_storage_handlers.exceptions import DataReadException, \
    DataWriteException


class BufferedFileDataStorage(AbstractBufferedDataStorage,
                              AbstractContextManager):
    """Data storage based on a temporary file with two pointers, one for
    reading and one for writing.
    """

    __slots__ = [
        # ??????????????
        "_filename",

        # ??????????????
        "_file_size",

        # ??????????????
        "_read_pointer",

        # ??????????????
        "_write_pointer",

        # ?????????
        "_file"
    ]

    def __init__(self, filename, mode):
        self._filename = filename
        self._file_size = 0
        self._read_pointer = 0
        self._write_pointer = 0

        # open the file using the real handler
        try:
            self._file = open(filename, mode)
        except IOError as e:
            raise DataReadException(
                "unable to open file {0}; {1}".format(filename, e))

    def write(self, data):
        if not (isinstance(data, bytearray) or isinstance(data, str)):
            raise DataWriteException(
                "data to write is not in a suitable format (bytearray or "
                "string). Current data format: {0:s}".format(type(data)))

        self._file.seek(self._write_pointer)

        try:
            self._file.write(data)
        except IOError as e:
            raise DataWriteException(
                "unable to write {0:d} bytes to file {1:s}: caused by {2}"
                .format(len(data), self._filename, e))

        self._file_size += len(data)
        self._write_pointer += len(data)

    def read(self, data_size):
        self._file.seek(self._read_pointer)

        try:
            data = self._file.read(data_size)
        except BlockingIOError as e:
            raise DataReadException(
                "unable to read {0:d} bytes from file {1:s}; {2}"
                .format(data_size, self._filename, e))

        self._read_pointer += data_size
        return data

    def readinto(self, data):
        """ See \
            :py:meth:`spinn_storage_handlers.abstract_classes.AbstractBufferedDataStorage.readinto`
        """
        self._file.seek(self._read_pointer)

        try:
            length = self._file.readinto(data)
        except BlockingIOError as e:
            raise IOError(
                "unable to read {0:d} bytes from file {1:s}; {2}"
                .format(len(data), self._filename, e))

        self._read_pointer += length
        return length

    def read_all(self):
        self._file.seek(0)
        data = self._file.read()
        self._read_pointer = self._file.tell()
        return data

    def seek_read(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self._read_pointer = offset
        elif whence == os.SEEK_CUR:
            self._read_pointer += offset
        elif whence == os.SEEK_END:
            self._read_pointer = self._file_size - abs(offset)

        if self._read_pointer < 0:
            self._read_pointer = 0

        file_len = self._file_len
        if self._read_pointer > file_len:
            self._read_pointer = file_len

    def seek_write(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self._write_pointer = offset
        elif whence == os.SEEK_CUR:
            self._write_pointer += offset
        elif whence == os.SEEK_END:
            self._write_pointer = self._file_size - abs(offset)

        if self._write_pointer < 0:
            self._write_pointer = 0

        file_len = self._file_len
        if self._write_pointer > file_len:
            self._write_pointer = file_len

    def tell_read(self):
        return self._read_pointer

    def tell_write(self):
        return self._write_pointer

    def eof(self):
        file_len = self._file_len
        return (file_len - self._read_pointer) <= 0

    def close(self):
        try:
            self._file.close()
        except Exception as e:
            DataReadException(
                "file {0} cannot be closed; {1}".format(self._filename, e))

    @property
    def _file_len(self):
        """The size of the file.

        :return: The size of the file
        :rtype: int
        """
        current_pos = self._file.tell()
        self._file.seek(0, 2)
        end_pos = self._file.tell()
        self._file.seek(current_pos)
        return end_pos

    @property
    def filename(self):
        """
        property method

        """
        return self._filename
