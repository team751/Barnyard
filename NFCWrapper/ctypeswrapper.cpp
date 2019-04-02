#include "sptag/nfc/taguidextractor.h"

extern "C" {
    sptag::nfc::TagUidExtractor *TagUidExtractor_new() {
        return new sptag::nfc::TagUidExtractor();
    }

    void TagUidExtractor_delete(sptag::nfc::TagUidExtractor *obj) {
        delete obj;
    }

    bool TagUidExtractor_init_device(sptag::nfc::TagUidExtractor *obj) {
        return obj->init_device();
    }

    wchar_t *TagUidExtractor_get_uid_from_next_tag(
                                            sptag::nfc::TagUidExtractor *obj) {
        return obj->get_uid_from_next_tag();
    }
}
