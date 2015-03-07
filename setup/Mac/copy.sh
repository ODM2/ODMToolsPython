#!/bin/bash


zip -r odmtools dist/ > /dev/null 

cp -rv odmtools.zip '/Volumes/VMware Shared Folders/VM share' > /dev/null 

open '/Volumes/VMware Shared Folders/VM share/odmtools.zip' > /dev/null

rm '/Volumes/VMware Shared Folders/VM share/odmtools.zip' odmtools.zip > /dev/null

echo "Done!"

