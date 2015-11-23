#!/bin/sh

while getopts d: o
   do case "$o" in
		d)  OUTPUTDIR="$OPTARG";;
		\?)  echo "Usage: $0 -d output_dir" && exit 1;;
	esac
done

swig -c++ -python -outdir . -o djonpythondriver.cpp driver-python.i

if [ ! -z "${OUTPUTDIR}" ]; 
then
	echo "Refreshing output dir $OUTPUTDIR"
	cp -R python/* $OUTPUTDIR
fi
