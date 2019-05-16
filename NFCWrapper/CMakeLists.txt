cmake_minimum_required(VERSION 3.7)
project(NFCWrapper)

set(CMAKE_CXX_STANDARD 14)

add_library(NFCWrapper SHARED ctypeswrapper.cpp sptag/nfc/taguidextractor.cpp)

TARGET_LINK_LIBRARIES(NFCWrapper nfc)