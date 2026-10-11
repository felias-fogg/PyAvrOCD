#!/bin/bash
#This is a script for packing the avrocd-link tools: avr-gdb + pyavrocd + pyavrocd-util + simavr.
#The archives will be uploaded as assests in each release and can be downloaded from there
#as https://github.com/felias-fogg/PyAvrOCD/releases/download/<version>/pyavrocd-<machine-type>.tar.gz.
#Additionally, the pyavrocd binaries will be uploaded stand-alone
#
#usage: call the script from the root folder; version will be deduced from pyavrocd -V

# upload-artifact packs into a ZIP, which loses the executable bit, so
# anything that travels through an artifact has to get it back. pyavrocd
# does today. simavr comes from the repository, where git keeps the bit --
# the second line is there for the day it goes through an artifact as
# well; the redirect swallows the complaint when a triple has no such file.
chmod +x extras/binaries/*/pyavrocd
chmod +x extras/binaries/*/bin/simavr 2>/dev/null

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
rm -rf avrocd-tools
mkdir assets
mkdir avrocd-tools

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
                echo {\"name\": \"tool-pyavrocd\", \"version\": \"${VERNUM}\", \"description\": \"Debugging tools for AVR microcontrollers: pyavrocd, avr-gdb, and simavr\", \"keywords\": [\"GDB server\", \"GDB client\", \"simulator\", \"debugging\", \"compiler\", \"microchip\", \"avr\"], \"homepage\": \"https://pyavrocd.io\", \"url\": \"https://github.com/felias-fogg/pyavrocd\", \"license\": \"MIT\", \"system\": \"${SYSTEM}\"} > tools/package.json
		cp -r $dir/* tools/
		# The simavr archives come from 'make install-simavr', so they also
		# carry its development files: the headers, the static library, the
		# pkg-config files and the bare .so symlink that only a linker uses.
		# A headless run needs none of it -- just bin/simavr, libsimavr.so.1
		# and the libelf/libz beside it -- and it is some 3.7 MB per package.
		rm -rf tools/include tools/lib/pkgconfig tools/lib/*.a \
		       tools/lib/libsimavr.so tools/lib/libsimavrparts.so
		# Downloaded archives arrive with com.apple.quarantine set, and
		# macOS tar stores extended attributes, so the flag would travel
		# into the package. Strip it from the staging copy. xattr exists
		# only on macOS, hence the guard -- on a Linux runner there is
		# nothing to strip in the first place.
		command -v xattr >/dev/null && xattr -r -d com.apple.quarantine tools 2>/dev/null || true
		tar -zc --exclude="*DS_Store" --exclude="*/._*" -f ./assets/avrocd-tools-${VERNUM}-${type}.tar.gz tools/
		rm -rf tools
                cp -r $dir/pyavrocd* tool/
                echo {\"name\": \"tool-pyavrocd\", \"version\": \"${VERNUM}\", \"description\": \"GDB server for AVR microcontrollers\", \"keywords\": [\"GDB server\", \"debugging\", \"compiler\", \"microchip\", \"avr\"], \"homepage\": \"https://pyavrocd.io\", \"url\": \"https://github.com/felias-fogg/pyavrocd\", \"license\": \"MIT\", \"system\": \"${SYSTEM}\"} > tool/package.json
                rm -rf tool/pyavrocd-util/svd
                if [[ $type == *"linux"* ]];then
                    rm -rf tool/pyavrocd-util
                fi
                command -v xattr >/dev/null && xattr -r -d com.apple.quarantine tool 2>/dev/null || true
                tar -zc --exclude="*DS_Store" --exclude="*/._*" -f ./assets/pyavrocd-${type}.tar.gz tool/
	    fi
	fi
    fi
done
cd ..

echo "Packing SVDs"
tar -zc --exclude "*DS_Store" --exclude="*/._*" -f extras/assets/svd.tar.gz svd/


