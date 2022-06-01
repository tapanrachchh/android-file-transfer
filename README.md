# adb-file-manager

<p>
<img src="images/logo_icon.png"" alt="scrcpy" align="right" />
</p>

Cross Platform Desktop app for android file transfer using adb

Features:

- Drag and Drop to transfer files

## Requirements

Make sure you [enabled adb debugging][enable-adb] on your device(s).

[enable-adb]: https://developer.android.com/studio/command-line/adb.html#Enabling

## Download

[<img alt="alt_text" width="40px" src="images/windows.ico" />](dist/ADB%20File%20Manager.exe?raw=1) [<img alt="alt_text" width="40px" src="images/linux-48.ico" />](dist/ADB%20File%20Manager%201.1.0%20-%20Linux%20-OLD_VERSION?raw=1) [<img alt="alt_text" width="40px" src="images/mac-os-48.ico" />](dist/ADB%20File%20Manager%201.1.0%20Mac%20App%20File%20%20-OLD_VERSION.zip?raw=1)

## Run Locally

Install requirements

```bash
  python install -r requirements.txt
```

Change the adb_path in main.py to adb executable path

```bash
  adb_path="/usr/local/bin/adb"

```

Run

```bash
  python main.py
```

## Build

```bash
  python -m PyInstaller main.spec
```
