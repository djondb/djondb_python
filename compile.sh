#!/bin/sh

while getopts j:d:u o
   do case "$o" in
	   u)  UPLOAD="true";;
		\?)  echo "Usage: $0 -u" && exit 1;;
	esac
done

#executes update to ensure .h files
rm -rf output
mkdir output
mkdir output/includes

OS=`uname -s`
if test "$OS" = "Darwin"; then
cp /usr/lib/libdjon-client.dylib /usr/lib/libdjon-client.dylib output/
else
cp /usr/lib/libdjon-client.so output/
fi

cp includes/*.h output/includes/
cp setup.py output/
cp pydjondb.py output/
cp MANIFEST.in output/
cp *.cpp output/

cd output
python setup.py build

if [ ! -z "${UPLOAD}" ]; 
then
	cd output
	python setup.py register
	#python setup.py build_ext --inplace
	python setup.py sdist upload
	#python setup.py bdist_dumb upload
	#python setup.py bdist_dumb upload
fi

