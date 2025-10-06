#!/bin/bash
#script for packing the avrocd-link tools: avr-gdb + pyavrocd + pyavrocd-util
#the packaged archives are found afterwards in the folders assets and avrocd-tools
#usage: call the script in this directory; version will be deduced from pyavrocd -V

chmod +x extras/binaries/arm64-apple-darwin/pyavrocd
chmod +x extras/binaries/aarch64-linux-gnu/pyavrocd
chmod +x extras/binaries/x86_64-apple-darwin/pyavrocd
chmod +x extras/binaries/x86_64-linux-gnu/pyavrocd

#assume that we are running on an Intel (compatible) runner
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    typestr="x86_64-linux-gnu"
elif
   [[ "$OSTYPE" == "darwin"* ]]; then
    typestr="x86_64-apple-darwin"
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
	if  [ -f $dir/avr-gdb -o -f $dir/avr-gdb.exe ]; then
	    if [ -f $dir/pyavrocd -o -f $dir/pyavrocd.exe ]; then
		if [ -d $dir/pyavrocd-util ]; then
		    type=${dir##*/}
		    echo "Packing tools for: $type"
		    rm -rf tools
		    mkdir tools
		    cp -r $dir/* tools/
		    tar -jcv --exclude="*DS_Store" --exclude="*/._*" -f ./avrocd-tools/avrocd-tools-${VERNUM}-${type}.tar.bz2 tools/
		    cd tools
		    if [ ! -f readme.md ]; then
			tar -zcv --exclude="*DS_Store" --exclude="*/._*" -f ../assets/pyavrocd-binary-${type}.tar.gz .
		    fi
		    cd ..
		    rm -rf tools
		fi
	    fi
	fi
    fi
done
cd ..


