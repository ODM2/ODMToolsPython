#!/bin/bash


echo "Building!!"
echo "cleanup"
if [ -d build ] && [ -d dist ]; then
	echo "Cleaning up old build and dist files"
	rm -r --interactive=once build dist
fi
echo "activate environment"
source activate odmtools
echo "run py2app"
sudo python ../setuptest.py py2app
#sudo /usr/local/Cellar/python/2.7.8/bin/python setup.py py2app
