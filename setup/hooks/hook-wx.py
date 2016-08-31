import os, sys
from PyInstaller.utils.hooks import collect_data_files


datas = collect_data_files('wx')

#datas += [(os.path.join(os.path.dirname(sys.executable), '../lib/libwx_osx_cocoau-3.0.0.0.0.dylib'), '.')]