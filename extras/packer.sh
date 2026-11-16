#!/bin/bash
#This is a script for packing the AVR debug tools: avr-gdb + pyavrocd + pyavrocd-util + simavr.
#The archives will be uploaded as assets in each release and can be downloaded from there
#as https://github.com/felias-fogg/PyAvrOCD/releases/download/<version>/avr-debugger-<version>-<machine-type>.tar.gz.
#Inside, all executables are in bin/, the simavr libraries in lib/, and the SVD files in svd/.
#Additionally, the pyavrocd binaries will be uploaded stand-alone
#
#usage: call the script from the root folder; version will be deduced from pyavrocd -V

# Stop at the first failure. Without it, a failed avr-gdb download went
# unnoticed: the script carried on and packed an archive without avr-gdb.
set -e

# upload-artifact packs into a ZIP, which loses the executable bit, so
# anything that travels through an artifact has to get it back. pyavrocd
# does today. simavr comes from the repository, where git keeps the bit --
# the second line is there for the day it goes through an artifact as
# well; the redirect swallows the complaint when a triple has no such file,
# and the '|| true' keeps that from ending the script under set -e.
chmod +x extras/binaries/*/pyavrocd
chmod +x extras/binaries/*/bin/simavr 2>/dev/null || true

#assume that we are running on a compatible runner
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    typestr=`arch`"-linux-gnu"
elif
   [[ "$OSTYPE" == "darwin"* ]]; then
    typestr=`arch`"-apple-darwin"
else
    echo "Incompatible runner"
    exit 1
fi

cd extras

if [ -f binaries/$typestr/pyavrocd ]; then
    VERSION=`binaries/$typestr/pyavrocd -V`
    VERNUM=`echo $VERSION | cut -d' ' -f 3`
    echo "Creating tool packages for version $VERNUM"
else
    echo "No PyAvrOCD binary found"
    cd ..
    exit 1
fi

rm -rf assets
mkdir assets

# And once on the working copies themselves: the archives are downloaded
# with a browser, so everything unpacked into binaries/ carries
# com.apple.quarantine until someone clears it. Doing it here keeps the
# repository clean as well, not just the staging copies below.
command -v xattr >/dev/null && xattr -r -d com.apple.quarantine binaries 2>/dev/null || true

for dir in binaries/*; do
    if [ -d $dir ]; then
	if [ -f $dir/pyavrocd -o -f $dir/pyavrocd.exe ]; then
	    if [ -d $dir/pyavrocd-util ]; then
		type=${dir##*/}
                if [[ $type == "aarch64-linux-gnu" ]]; then
                    SYSTEM="linux_aarch64"
                elif [[ $type == "arm-linux-gnueabihf" ]]; then
                    SYSTEM="linux_armv6l"
                elif [[ $type == "arm64-apple-darwin" ]]; then
                    SYSTEM="darwin_arm64"
                elif [[ $type == "i686-linux-gnu" ]]; then
                    SYSTEM="linux_i686"
                elif [[ $type == "i686-mingw32" ]]; then
                    SYSTEM="windows_x86"
                elif [[ $type == "x86_64-apple-darwin" ]]; then
                    SYSTEM="darwin_x86_64"
                elif [[ $type == "x86_64-linux-gnu" ]]; then
                    SYSTEM="linux_x86_64"
                elif [[ $type == "x86_64-mingw32" ]]; then
                    SYSTEM="windows_amd64"
                else
                    echo "Unknown OS type: $type"
                    exit 1
                fi
		# What the build measured about itself, written by the release
		# workflow's floor check. Missing -- an older artifact, or a folder
		# filled by hand -- means the field is left out rather than guessed.
		if [ -f $dir/SYSTEM_BASELINE ]; then
		    BASEFRAG="\"systemBaseline\": \"$(cat $dir/SYSTEM_BASELINE)\", "
		    echo "System baseline: $(cat $dir/SYSTEM_BASELINE)"
		else
		    BASEFRAG=""
		    echo "No SYSTEM_BASELINE in $dir, package.json will not carry one"
		fi
		echo "Packing tools for: $type"
		rm -rf tools
                rm -rf tool
		mkdir tools
                mkdir tool
                pushd $dir
                wget https://github.com/felias-fogg/avr-gdb/releases/latest/download/${type}.tar.gz
                tar xvzf ${type}.tar.gz
                mv tool/avr-gdb* .
                rm -rf tool
                rm -f ${type}.tar.gz
                popd
                echo {\"name\": \"tool-pyavrocd\", \"version\": \"${VERNUM}\", \"description\": \"Debugging tools for AVR microcontrollers: pyavrocd, avr-gdb, and simavr\", \"keywords\": [\"GDB server\", \"GDB client\", \"simulator\", \"debugging\", \"compiler\", \"microchip\", \"avr\"], \"homepage\": \"https://pyavrocd.io\", \"url\": \"https://github.com/felias-fogg/pyavrocd\", \"license\": \"MIT\", ${BASEFRAG}\"system\": \"${SYSTEM}\"} > tools/package.json
		cp -r $dir/* tools/
		# All executables go into bin/, where simavr already is: pyavrocd
		# with its pyavrocd-util beside it (PyInstaller's onedir needs the
		# two side by side), and avr-gdb, which is a single file. lib/ stays
		# a sibling of bin/, because simavr finds its libraries on Linux
		# through an RPATH of $ORIGIN/../lib.
		mkdir -p tools/bin
		mv tools/pyavrocd* tools/avr-gdb* tools/bin/
		# The SVDs are for the IDE's register view only (the server takes its
		# register descriptions from the device modules), so they sit at the top,
		# beside bin/: {runtime.tools.avr-debugger.path}/svd/<mcu>.svd. They come
		# from the repository; a build made before the spec stopped bundling them
		# still has a copy in pyavrocd-util, which goes.
		rm -rf tools/bin/pyavrocd-util/svd
		cp -r ../svd tools/svd
		# The simavr archives come from 'make install-simavr', so they also
		# carry its development files: the headers, the static library, the
		# pkg-config files and the bare .so symlink that only a linker uses.
		# A headless run needs none of it -- just bin/simavr, lib/libsimavr.so.1
		# and the libelf/libz beside it -- and it is some 3.7 MB per package.
		rm -rf tools/include tools/lib/pkgconfig tools/lib/*.a \
		       tools/lib/libsimavr.so tools/lib/libsimavrparts.so
		# Downloaded archives arrive with com.apple.quarantine set, and
		# macOS tar stores extended attributes, so the flag would travel
		# into the package. Strip it from the staging copy. xattr exists
		# only on macOS, hence the guard -- on a Linux runner there is
		# nothing to strip in the first place.
		command -v xattr >/dev/null && xattr -r -d com.apple.quarantine tools 2>/dev/null || true
		tar -zc --exclude="*DS_Store" --exclude="*/._*" -f ./assets/avr-debugger-${VERNUM}-${type}.tar.gz tools/
		rm -rf tools
                cp -r $dir/pyavrocd* tool/
                echo {\"name\": \"tool-pyavrocd\", \"version\": \"${VERNUM}\", \"description\": \"GDB server for AVR microcontrollers\", \"keywords\": [\"GDB server\", \"debugging\", \"compiler\", \"microchip\", \"avr\"], \"homepage\": \"https://pyavrocd.io\", \"url\": \"https://github.com/felias-fogg/pyavrocd\", \"license\": \"MIT\", ${BASEFRAG}\"system\": \"${SYSTEM}\"} > tool/package.json
                # The stand-alone server does not need the SVD files: those are for
                # the IDE's register view, which gets them from the tools package
                # above. The spec no longer bundles them; the rm is for a build
                # made before that. Everything else in pyavrocd-util stays -- it holds
                # libpython and the extension modules. Linux used to have the whole
                # folder removed here, which was right while staticx made a single
                # file out of the build, but since 1.6.0 (staticx gone, onedir on
                # every platform) it left an executable that cannot start.
                rm -rf tool/pyavrocd-util/svd
                command -v xattr >/dev/null && xattr -r -d com.apple.quarantine tool 2>/dev/null || true
                tar -zc --exclude="*DS_Store" --exclude="*/._*" -f ./assets/pyavrocd-${type}.tar.gz tool/
	    fi
	fi
    fi
done
cd ..

echo "Packing SVDs"
tar -zc --exclude "*DS_Store" --exclude="*/._*" -f extras/assets/svd.tar.gz svd/


