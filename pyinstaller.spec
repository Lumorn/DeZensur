# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['dez.py'],
    pathex=['.'],
    binaries=[],
    datas=[('models', 'models'), ('gui/dist', 'gui/dist')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='dezensor',
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='dezensor',
)
