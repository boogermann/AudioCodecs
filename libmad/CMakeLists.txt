cmake_minimum_required (VERSION 3.2)
project(libMAD VERSION 0.15.1 LANGUAGES C)

include(TestBigEndian)
include(${CMAKE_CURRENT_SOURCE_DIR}/../audio_codec_common.cmake)

TEST_BIG_ENDIAN(WORDS_BIGENDIAN)
if(WORDS_BIGENDIAN)
    add_definitions(-DWORDS_BIGENDIAN=1)
endif()

if(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
    # Turn on warnings and legacy C/C++ standards to support more compilers
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wno-pedantic -std=c99")
endif()

if(MSVC)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /wd4244 /wd4146")
endif()

add_definitions(
    -DFPM_DEFAULT
    -DHAVE_CONFIG_H
)

add_library(mad STATIC
    src/bit.c
    src/decoder.c
    src/fixed.c
    src/frame.c
    src/huffman.c
    src/layer12.c
    src/layer3.c
    src/stream.c
    src/synth.c
    src/timer.c
    src/version.c
)

target_include_directories(mad PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

install(TARGETS mad
        LIBRARY DESTINATION "lib"
        ARCHIVE DESTINATION "lib"
        INCLUDES DESTINATION "include")

install(FILES
        include/mad.h
        DESTINATION include/)

