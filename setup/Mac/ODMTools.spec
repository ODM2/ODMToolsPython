# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/stephanie/DEV/ODMToolsPython/ODMTools.py'],
             pathex=['/Users/stephanie/DEV/ODMToolsPython/setup/Mac'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ODMTools',
          debug=False,
          strip=None,
          upx=True,
          console=False , version='/Users/stephanie/DEV/ODMToolsPython/setup/version.txt', icon='odmtools/common/icons/ODMTools.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='ODMTools')
app = BUNDLE(coll,
             name='ODMTools.app',
             icon='odmtools/common/icons/ODMTools.icns',
             bundle_identifier=None)
