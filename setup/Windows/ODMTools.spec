

a = Analysis(['D:\\DEV\\ODMTools\\ODMTools.py'],
             pathex=['D:\\DEV\\ODMTools\\setup\\Windows'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=['../hooks'],
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
          upx=False,
          console=True , version='D:\\DEV\\ODMTools\\setup\\version.txt', icon='D:\\DEV\\ODMTools\odmtools\\common\\icons\\ODMTools.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ODMTools')




# -*- mode: python -*-

block_cipher = None


a = Analysis(['ODMTools.py'],
             pathex=['D:\\DEV\\ODMTools'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ODMTools')
