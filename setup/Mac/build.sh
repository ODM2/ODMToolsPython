#!/bin/bash


echo "Building!!"
if [ -d build ] && [ -d dist ]; then
	echo "Cleaning up old build and dist files"
	rm -ir build dist
fi

sudo python setup.py py2app
#sudo /usr/local/Cellar/python/2.7.8/bin/python setup.py py2app
