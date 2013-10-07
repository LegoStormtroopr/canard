# -*- mode: python -*-
a = Analysis(['canard_main.py'],
             pathex=['C:\\Users\\theodore\\My Documents\\GitHub\\canard'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Canard.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icons\\Canard_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Canard')
