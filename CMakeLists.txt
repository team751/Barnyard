cmake_minimum_required(VERSION 3.7.2)
project(SpaceTag)

set(CMAKE_CXX_STANDARD 14)

add_executable(SpaceTag main.cpp ../spacetagnfcwrapper/sptag/nfc/taguidextractor.cpp ../spacetagnfcwrapper/sptag/nfc/taguidextractor.h)

TARGET_LINK_LIBRARIES(SpaceTag nfc)