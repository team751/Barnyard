cmake_minimum_required(VERSION 3.12)
project(SpaceTag)

set(CMAKE_CXX_STANDARD 14)

add_executable(SpaceTag main.cpp sptag/nfc/taguidextractor.cpp sptag/nfc/taguidextractor.h)

TARGET_LINK_LIBRARIES(SpaceTag nfc)