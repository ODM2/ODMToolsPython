# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/stephanie/DEV/ODMToolsPython/ODMTools.py'],
             pathex=['/Users/stephanie/DEV/ODMToolsPython/setup/Mac'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=['/Users/stephanie/DEV/ODMToolsPython/setup/hooks'],
             runtime_hooks=None,
             excludes=['PyQt4', 'PyQt4.QtCore', 'PyQt4.QtGui'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ODMTools',
          debug=False,
          strip=False,
          upx=True,
          console=False , version='/Users/stephanie/DEV/ODMToolsPython/setup/version.txt', icon='/Users/stephanie/DEV/ODMToolsPython/odmtools/common/icons/ODMTools.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='ODMTools')
app = BUNDLE(coll,
             name='ODMTools.app',
             icon='/Users/stephanie/DEV/ODMToolsPython/odmtools/common/icons/ODMTools.icns',
             bundle_identifier=None)
