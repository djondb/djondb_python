#!/bin/sh

while getopts j:d:u o
   do case "$o" in
	   u)  UPLOAD="true";;
		\?)  echo "Usage: $0 -u" && exit 1;;
	esac
done

#executes update to ensure .h files
sh update.sh
cd python
cp ../*.h .

rm -rf output
mkdir output
mkdir output/include

cp ../*.h output/include/

OS=`uname -s`
if test "$OS" = "Darwin"; then
cp ../../../build/usr/lib/libdjon-client.0.dylib ../../obj/usr/lib/libdjon-client.dylib output/
else
cp ../../../build/usr/lib/libdjon-client.so output/
fi

swig -c++ -python -outdir output -o output/djonpythondriver.cpp ../driver-python.i

cp setup.py output/
cp MANIFEST.in output/

if [ ! -z "${UPLOAD}" ]; 
then
	cd output
	python setup.py register
	#python setup.py build_ext --inplace
	python setup.py sdist upload
	#python setup.py bdist_dumb upload
	#python setup.py bdist_dumb upload
fi

