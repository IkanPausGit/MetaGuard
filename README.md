# MetaGuard

## Detector

- Detects predefined sensitive metadata fields in JPEG, PNG, PDF and DOCX files and shows an illustrative privacy risk score.

## Setup

Open a terminal in this version's folder. The included dependencies were tested with Python 3.14.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Try it

```powershell
.\.venv\Scripts\python.exe main.py
```

Confirm authorization and enter `gps_test.jpg` at the file name prompt.
