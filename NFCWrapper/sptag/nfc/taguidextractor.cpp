//
// Created by bobby on 10/14/18.
//

#include <sstream>
#include "taguidextractor.h"

namespace sptag {
    namespace nfc {
        TagUidExtractor::~TagUidExtractor() {
            if(m_nfc_context != nullptr) {
                nfc_exit(m_nfc_context);
            }

            if(m_nfc_reader != nullptr) {
                nfc_close(m_nfc_reader);
            }
        }

        bool TagUidExtractor::init_device() {
            nfc_init(&m_nfc_context);
            if(m_nfc_context == nullptr) {
                std::cerr << "ERROR: Unable to initialize a libnfc context!\n";
                return false;
            }

            std::clog << "SpaceTag v0.0.1 using libnfc " << nfc_version()
                      << "\n";
            std::clog << "Opening default nfc device...\n";

            m_nfc_reader = nfc_open(m_nfc_context, nullptr);

            if(m_nfc_reader == nullptr) {
                std::cerr << "ERROR: Unable to open default nfc device.\n";
                return false;
            }

            std::clog << "SpaceTag opened and is now using NFC Reader "
                      << nfc_device_get_name(m_nfc_reader) << "\n";

            if(nfc_initiator_init(m_nfc_reader) < 0) {
                std::cerr << "ERROR: Unable to set NFC Reader to initiator "
                          << "mode\n";
                std::cerr << "libnfc says error was ";
                nfc_perror(m_nfc_reader, "nfc_initiator_init");
                return false;
            }

            return true;
        }

        long TagUidExtractor::get_uid_from_next_tag() {

            if(m_nfc_reader == nullptr) {
                return-1;
            }

            const nfc_modulation nfc_mod_mifare = {
                .nmt = NMT_ISO14443A,
                .nbr = NBR_106,
            };
            if(nfc_initiator_select_passive_target(m_nfc_reader,
                    nfc_mod_mifare, NULL, 0, &m_past_nfc_tag)) {
                std::string uid_string_buffer;

                unsigned long return_value;

                for(uint8_t byte : m_past_nfc_tag.nti.nai.abtUid) {
                    // Get integer value of char NOT actual character
                    // representation
                    uid_string_buffer.append(std::to_string(
                            static_cast<int>(byte)));
                }

                std::cout << uid_string_buffer << "\n";
                return std::atol(uid_string_buffer.c_str());
            } else {
                return -1;
            }
        }
    }
}
