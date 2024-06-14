import PyInstaller.__main__

PyInstaller.__main__.run([
    'tempus/main.py',
    '--onedir',
    '--w',
    '--icon="tempus/resources/icons/icon.png"'
])
