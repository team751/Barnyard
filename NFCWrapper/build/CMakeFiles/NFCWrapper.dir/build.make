# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.7

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pi/spacetag/NFCWrapper

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pi/spacetag/NFCWrapper/build

# Include any dependencies generated for this target.
include CMakeFiles/NFCWrapper.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/NFCWrapper.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/NFCWrapper.dir/flags.make

CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o: CMakeFiles/NFCWrapper.dir/flags.make
CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o: ../ctypeswrapper.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pi/spacetag/NFCWrapper/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o -c /home/pi/spacetag/NFCWrapper/ctypeswrapper.cpp

CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pi/spacetag/NFCWrapper/ctypeswrapper.cpp > CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.i

CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pi/spacetag/NFCWrapper/ctypeswrapper.cpp -o CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.s

CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o.requires:

.PHONY : CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o.requires

CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o.provides: CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o.requires
	$(MAKE) -f CMakeFiles/NFCWrapper.dir/build.make CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o.provides.build
.PHONY : CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o.provides

CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o.provides.build: CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o


CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o: CMakeFiles/NFCWrapper.dir/flags.make
CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o: ../sptag/nfc/taguidextractor.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pi/spacetag/NFCWrapper/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o -c /home/pi/spacetag/NFCWrapper/sptag/nfc/taguidextractor.cpp

CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pi/spacetag/NFCWrapper/sptag/nfc/taguidextractor.cpp > CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.i

CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pi/spacetag/NFCWrapper/sptag/nfc/taguidextractor.cpp -o CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.s

CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o.requires:

.PHONY : CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o.requires

CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o.provides: CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o.requires
	$(MAKE) -f CMakeFiles/NFCWrapper.dir/build.make CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o.provides.build
.PHONY : CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o.provides

CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o.provides.build: CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o


# Object files for target NFCWrapper
NFCWrapper_OBJECTS = \
"CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o" \
"CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o"

# External object files for target NFCWrapper
NFCWrapper_EXTERNAL_OBJECTS =

libNFCWrapper.so: CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o
libNFCWrapper.so: CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o
libNFCWrapper.so: CMakeFiles/NFCWrapper.dir/build.make
libNFCWrapper.so: CMakeFiles/NFCWrapper.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pi/spacetag/NFCWrapper/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX shared library libNFCWrapper.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/NFCWrapper.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/NFCWrapper.dir/build: libNFCWrapper.so

.PHONY : CMakeFiles/NFCWrapper.dir/build

CMakeFiles/NFCWrapper.dir/requires: CMakeFiles/NFCWrapper.dir/ctypeswrapper.cpp.o.requires
CMakeFiles/NFCWrapper.dir/requires: CMakeFiles/NFCWrapper.dir/sptag/nfc/taguidextractor.cpp.o.requires

.PHONY : CMakeFiles/NFCWrapper.dir/requires

CMakeFiles/NFCWrapper.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/NFCWrapper.dir/cmake_clean.cmake
.PHONY : CMakeFiles/NFCWrapper.dir/clean

CMakeFiles/NFCWrapper.dir/depend:
	cd /home/pi/spacetag/NFCWrapper/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pi/spacetag/NFCWrapper /home/pi/spacetag/NFCWrapper /home/pi/spacetag/NFCWrapper/build /home/pi/spacetag/NFCWrapper/build /home/pi/spacetag/NFCWrapper/build/CMakeFiles/NFCWrapper.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/NFCWrapper.dir/depend

