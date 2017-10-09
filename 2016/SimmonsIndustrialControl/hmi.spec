# -*- mode: python -*-

block_cipher = None


a = Analysis(['hmi.py'],
             pathex=['C:\\Users\\mithompson\\Desktop\\hmi'],
             binaries=None,
             datas=[('.','.')],
             hiddenimports=['cherrypy.wsgiserver.wsgiserver3'],
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
          name='hmi',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='favicon.ico')
