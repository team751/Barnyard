cmake_minimum_required(VERSION 3.12)
project(NFCWrapper)

set(CMAKE_CXX_STANDARD 14)

add_library(NFCWrapper SHARED ctypeswrapper.cpp)

TARGET_LINK_LIBRARIES(NFCWrapper nfc)