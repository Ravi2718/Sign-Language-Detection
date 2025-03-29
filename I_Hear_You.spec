# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add all your data files here
datas = [
    # Model files
    ('Model/keras_model.h5', 'Model'),
    ('Model/labels.txt', 'Model'),

    # Video files
    ('Transulator/sign video/*.mp4', 'Transulator/sign video'),

    # Image files
    ('image/sign/*.jpg', 'image/sign'),
    ('image/video call/*.png', 'image/video call'),
    ('image/*.png', 'image'),

    # Sound files
    ('Sound/end_sound.mp3', 'Sound'),
]

a = Analysis(
    ['index.py'],  # Main script
    pathex=['E:\\SNS IT\\final project\\NSLD'],  # Path to your project
    binaries=[],
    datas=datas,  # Include all data files
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    name='I_Hear_You',  # Name of the output executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you want a console window
    icon='E:\\SNS IT\\final project\\NSLD\\logo.ico',  # Path to your icon file
)