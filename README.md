# adb-file-manager

<p>
<img src="images/logo_icon.png"" alt="scrcpy" align="right" />
</p>

Android file transfer using adb

- Drag and Drop to transfer files

## Requirements

Make sure you [enabled adb debugging][enable-adb] on your device(s).

[enable-adb]: https://developer.android.com/studio/command-line/adb.html#Enabling

## Run Locally

Install requirements

```bash
  pip3 install -r requirements.txt
```

Run

```bash
  python main.py
```

## Build

```bash
  python -m PyInstaller main.spec
```
