#include "sptag/nfc/taguidextractor.h"

int main() {
    sptag::nfc::TagUidExtractor tag_uid_extractor;

    if(tag_uid_extractor.init_device()) {
        std::clog << "UID recieved = " << tag_uid_extractor.get_uid_from_next_tag() << "\n";
    }
}
