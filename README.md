# MetaGuard v0.2

## HTML reporting

- Detects predefined sensitive metadata fields in JPEG, PNG, PDF and DOCX files and shows an illustrative privacy risk score.
- Generates a local HTML report with metadata, findings and recommendations.

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
To generate a report, answer `yes` at the report prompt and open the HTML file in `output/`.
