from ctypes import c_bool
from ctypes import c_wchar_p
from ctypes import c_void_p
from ctypes import cdll


class TagUidExtractor:
    _nfc_library = None
    _obj = None

    def __init__(self, nfc_library_path):
        self._nfc_library = cdll.LoadLibrary(nfc_library_path)
        self._nfc_library.TagUidExtractor_new.restype = c_void_p
        self._obj = self._nfc_library.TagUidExtractor_new()

    def init_device(self):
        self._nfc_library.TagUidExtractor_init_device.argtypes = [c_void_p]
        self._nfc_library.TagUidExtractor_init_device.restype = c_bool

        return self._nfc_library.TagUidExtractor_init_device(self._obj)

    def get_uid_from_next_tag(self):
        self._nfc_library.TagUidExtractor_get_uid_from_next_tag.argtypes = [
                                                                    c_void_p]
        self._nfc_library.TagUidExtractor_get_uid_from_next_tag.restype = \
                                                                       c_wchar_p

        return self._nfc_library.TagUidExtractor_get_uid_from_next_tag(self._obj)
