# -*- mode: python ; coding: utf-8 -*-

import os
_here = os.path.abspath('.')
_img = os.path.join(_here, 'images')
_datas = []
if os.path.isdir(_img):
    for f in os.listdir(_img):
        if f.lower().endswith(('.png', '.ico')):
            _datas.append((os.path.join(_img, f), 'images'))

a = Analysis(
    ['matrix.py'],
    pathex=[],
    binaries=[],
    datas=_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Niko_Matrix',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[os.path.join(_img, 'icon.ico')],
    uac_admin=True,
)
