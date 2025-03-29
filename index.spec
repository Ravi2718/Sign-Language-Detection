# index.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add all your data files here
datas = [
    ('index2.py', '.'),  # Include other Python files
    ('test.py', '.'),
    ('dataset.py', '.'),
    ('dataset.sql', '.'),
    ('Model/keras_model.h5', 'Model'),
    ('Model/labels.txt', 'Model'),
    ('Transulator/sign video/hello.mp4', 'Transulator/sign video'),
    ('Transulator/sign video/My.mp4', 'Transulator/sign video'),
    ('Transulator/sign video/I Love You.mp4', 'Transulator/sign video'),
    ('Transulator/sign video/Food.mp4', 'Transulator/sign video'),
    ('image/sign/hello.jpg', 'image/sign'),
    ('image/sign/My.jpg', 'image/sign'),
    ('image/sign/I love you.jpg', 'image/sign'),
    ('image/sign/Food.jpg', 'image/sign'),
    ('image/video call/video.png', 'image/video call'),
    ('image/video call/image.png', 'image/video call'),
    ('image/video call/chevron-down.png', 'image/video call'),
    ('image/video call/image 1.png', 'image/video call'),
    ('image/video call/background.png', 'image/video call'),
    ('image/eye open.png', 'image'),
    ('image/close-eye.png', 'image'),
    ('image/login.png', 'image'),
    ('image/logo.png', 'image'),
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