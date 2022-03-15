# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [
('./images/back.png', './images/back.png', 'DATA'),
('./images/file.png', './images/file.png', 'DATA'),
('./images/folder.png', './images/folder.png', 'DATA'),
('./images/logo.png', './images/logo.png', 'DATA'),
('./images/tri.png', './images/tri.png', 'DATA'),
('./images/exclude.png', './images/exclude.png', 'DATA'),
('./images/push.png', './images/push.png', 'DATA'),
('./images/loader.gif', './images/loader.gif', 'DATA'),

]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)



if sys.platform == 'darwin':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='ADB File Manager',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False,
            icon='images/logo.icns')

if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='ADB File Manager.app',
                version='1.1.0',
                info_plist={
                  'NSHighResolutionCapable': 'True'
                },
                icon='images/logo.icns')

