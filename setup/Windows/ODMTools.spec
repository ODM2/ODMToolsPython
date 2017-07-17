# -*- mode: python -*-

block_cipher = None


a = Analysis(['D:\\DEV\\ODMTools\\ODMTools.py'],
             pathex=['D:\\DEV\\ODMTools\\setup\\Windows'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ODMTools',
          debug=False,
          strip=False,
          upx=False,
          console=True , version='D:\\DEV\\ODMTools\\setup\\version.txt', icon='odmtools\\common\\icons\\ODMTools.ico')
