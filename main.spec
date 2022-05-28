# -*- mode: python ; coding: utf-8 -*-


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
('./images/back-white.png', './images/back-white.png', 'DATA'),
('./images/folder.png', './images/folder.png', 'DATA'),
('./images/logo.png', './images/logo.png', 'DATA'),
('./images/peak.png', './images/peak.png', 'DATA'),
('./images/exclude.png', './images/exclude.png', 'DATA'),
('./images/push.png', './images/push.png', 'DATA'),
('./tools/win/adb.exe', './tools/win/adb.exe', 'DATA'),
('./tools/win/AdbWinApi.dll', './tools/win/AdbWinApi.dll', 'DATA'),
('./tools/win/AdbWinUsbApi.dll', './tools/win/AdbWinUsbApi.dll', 'DATA'),
('./images/process_file_transfer.gif', './images/process_file_transfer.gif', 'DATA'),
('./images/process_general.gif', './images/process_general.gif', 'DATA'),
]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='ADB File Manager',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='images/logo.ico'
           )
