#!/bin/bash
#This is a script for packing the avrocd-link tools: avr-gdb + pyavrocd + pyavrocd-util + simavr.
#The archives will be uploaded as assests in each release and can be downloaded from there
#as https://github.com/felias-fogg/PyAvrOCD/releases/download/<version>/pyavrocd-<machine-type>.tar.gz.
#Additionally, the pyavrocd binaries will be uploaded stand-alone
#
#usage: call the script from the root folder; version will be deduced from pyavrocd -V

chmod +x extras/binaries/*/pyavrocd

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
                echo {\"name\": \"avrocd-tools\", \"version\": \"${VERNUM}\", \"description\": \"Debugging tools for AVR microcontrollers: pyavrocd, avr-gdb, and simavr\", \"keywords\": [\"GDB server\", \"GDB client\", \"simulator\", \"debugging\", \"compiler\", \"microchip\", \"avr\"], \"homepage\": \"https://pyavrocd.io\", \"url\": \"https://github.com/felias-fogg/pyavrocd\", \"license\": \"MIT\", \"system\": \"${SYSTEM}\"} > tools/package.json
		cp -r $dir/* tools/
		tar -zc --exclude="*DS_Store" --exclude="*/._*" -f ./assets/avrocd-tools-${VERNUM}-${type}.tar.gz tools/
		rm -rf tools
                cp -r $dir/pyavrocd* tool/
                echo {\"name\": \"pyavrocd\", \"version\": \"${VERNUM}\", \"description\": \"GDB server for AVR microcontrollers\", \"keywords\": [\"GDB server\", \"debugging\", \"compiler\", \"microchip\", \"avr\"], \"homepage\": \"https://pyavrocd.io\", \"url\": \"https://github.com/felias-fogg/pyavrocd\", \"license\": \"MIT\", \"system\": \"${SYSTEM}\"} > tool/package.json
                rm -rf tool/pyavrocd-util/svd
                if [[ $type == *"linux"* ]];then
                    rm -rf tool/pyavrocd-util
                fi
                tar -zc --exclude="*DS_Store" --exclude="*/._*" -f ./assets/pyavrocd-${type}.tar.gz tool/
	    fi
	fi
    fi
done
cd ..

echo "Packing SVDs"
tar -zc --exclude "*DS_Store" --exclude="*/._*" -f extras/assets/svd.tar.gz svd/


