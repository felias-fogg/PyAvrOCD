#!/bin/bash
#This is a script for packing the avrocd-link tools: avr-gdb + pyavrocd + pyavrocd-util.
#The archives will be uploaded as assests in each release and can be downloaded from there
#as https://github.com/felias-fogg/PyAvrOCD/releases/download/<version>/pyavrocd-<machine-type>.tar.gz
#
#usage: call the script from the root folder; version will be deduced from pyavrocd -V

if [ -f extras/binaries/arm64-apple-darwin/pyavrocd ]; then
    chmod +x extras/binaries/arm64-apple-darwin/pyavrocd
fi
if [ -f extras/binaries/aarch64-linux-gnu/pyavrocd ]; then
    chmod +x extras/binaries/aarch64-linux-gnu/pyavrocd
fi
if [ -f extras/binaries/x86_64-apple-darwin/pyavrocd ]; then
    chmod +x extras/binaries/x86_64-apple-darwin/pyavrocd
fi
if [ -f  extras/binaries/x86_64-linux-gnu/pyavrocd ]; then
    chmod +x extras/binaries/x86_64-linux-gnu/pyavrocd
fi

#assume that we are running on an Intel (compatible) runner
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
                    SYSTEM="window_x86"
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
		mkdir tools
                echo {\"name\": \"tool-pyavrocd\", \"version\": \"${VERNUM}\", \"description\": \"GDB server for AVR microcontrollers\", \"keywords\": [\"GDB server\", \"debugging\", \"compiler\", \"microchip\", \"avr\"], \"homepage\": \"https://pyavrocd.io\", \"license\": \"GPL-3.0\", \"system\": \"${SYSTEM}\"} > tools/package.json
                if [ ! -f $dir/avr-gdb ] && [ ! -f $dir/avr-gdb.exe ]; then
                    pushd $dir
                    wget https://github.com/felias-fogg/avr-gdb/releases/latest/download/${type}.tar.gz
                    tar xvzf ${type}.tar.gz
                    rm -f ${type}.tar.gz
                    popd
                fi
		cp -r $dir/* tools/
		tar -zcv --exclude="*DS_Store" --exclude="*/._*" -f ./assets/avrocd-tools-${VERNUM}-${type}.tar.gz tools/
		rm -rf tools
	    fi
	fi
    fi
done
cd ..

echo "Packing SVDs"
tar -zcv --exclude "*DS_Store" --exclude="*/._*" -f extras/assets/svd.tar.gz svd/


