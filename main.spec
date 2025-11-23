# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    [],
    exclude_binaries=True,
    name='TikzGraphGen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    icon='./src/image.ico',
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    #icon='./src/image.ico',
    upx_exclude=[],
    name='TikzGraphGen',
)

print('Copying icon photo...')
f = open('./src/image.png', 'rb')
ft = open('./dist/TikzGraphGen/image.png', 'wb')
ft.write(f.read())
ft.close()
f.close()
