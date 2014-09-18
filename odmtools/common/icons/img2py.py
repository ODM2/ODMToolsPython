
#!/usr/bin/env python
"""This module contains a simple function to encode any number of
bitmap files to a .py file"""

import glob
import os
import re

from wx.tools import img2py

output = 'icons4addpoint.py'

# get the list of BMP files
#files = [f for f in os.listdir('.') if re.search(r'odm\d*x\d*\.png', f)]
#files = [f for f in os.listdir('.') if re.search('gtk-execute', f)]
files = glob.glob('*.png') #TODO: chose your extension here

open(output, 'w')

# call img2py on each file
for file in files:
    print "files: ", file


    # extract the basename to be used as the image name
    name = os.path.splitext(os.path.basename(file))[0]

    # encode it
    if file == files[0]:
        cmd = "-u -i -n %s %s %s" % (name, file, output)
    else:
        cmd = "-a -u -i -n %s %s %s" % (name, file, output)
    img2py.main(cmd.split())
