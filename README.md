# MetaGuard v0.4

## File comparison

- Detects predefined sensitive metadata fields in JPEG, PNG, PDF and DOCX files and shows an illustrative privacy risk score.
- Generates a local HTML report with metadata, findings and recommendations.
- Creates a cleaned copy and shows the privacy risk score before and after sanitization.
- Compares metadata in two files of the same format and lists added, removed, changed and unchanged fields.

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

Confirm authorization and enter `sample3.docx` at the file name prompt.
To try the comparison, answer `yes` and enter `modified.docx`.
To try sanitization, answer `yes` at the sanitization prompt. The cleaned copy goes to `output/`.
To generate a report, answer `yes` at the report prompt and open the HTML file in `output/`.
