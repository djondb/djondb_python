#!/bin/sh

while getopts j:d:us o
   do case "$o" in
      s) SWIG="true";;
	   u)  UPLOAD="true";;
		\?)  echo "Usage: $0 -u" && exit 1;;
	esac
done

if [ ! -z "${SWIG}" ]; 
then
   echo "Generating source files"
   swig -c++ -python -outdir . -o djonpythondriver.cpp driver-python.i
fi

#executes update to ensure .h files
sh update.sh
rm -rf output
mkdir output
mkdir output/includes

OS=`uname -s`
if test "$OS" = "Darwin"; then
cp /usr/local/lib/libdjon-client.dylib output/
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

