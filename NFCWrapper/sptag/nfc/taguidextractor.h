//
// Created by bobby on 10/14/18.
//

#ifndef SPACETAG_TAGUIDEXTRACTOR_H
#define SPACETAG_TAGUIDEXTRACTOR_H

#include <cmath>

#include <iostream>

#include <nfc/nfc.h>

namespace sptag {
    namespace nfc {
        class TagUidExtractor {
        public:
            TagUidExtractor() {}
            virtual ~TagUidExtractor();

            bool init_device();

            long get_uid_from_next_tag();

        private:
            nfc_device *m_nfc_reader;
            nfc_target m_past_nfc_tag;

            nfc_context *m_nfc_context;
        };
    }
}


#endif //SPACETAG_TAGUIDEXTRACTOR_H
