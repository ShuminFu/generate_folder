# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['cleanup.py'],
    pathex=[],
    binaries=[
        # 添加 tcl86t.dll 和 tk86t.dll
        ('libs/tcl86t.dll', '.'),
        ('libs/tk86t.dll', '.'),
    ],
    datas=[],
    hiddenimports=['_tkinter'],
    hookspath=['.'],
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
    name='cleanup',
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
    icon='static/folder.ico'
)
