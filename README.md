# MetaGuard v0.5

## Professional Command-Line Interface (CLI)

- Detects predefined sensitive metadata fields in JPEG, PNG, PDF and DOCX files and shows an illustrative privacy risk score.
- Generates a local HTML report with metadata, findings and recommendations.
- Creates a cleaned copy and shows the privacy risk score before and after sanitization.
- Compares metadata in two files of the same format and lists added, removed, changed and unchanged fields.
- Adds `--scan`, `--report`, `--sanitize`, `--compare` and `--help` while keeping the interactive workflow.

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

## Command-line examples

```powershell
.\.venv\Scripts\python.exe main.py --help
.\.venv\Scripts\python.exe main.py --scan samples/gps_test.jpg
.\.venv\Scripts\python.exe main.py --scan samples/sample2.pdf --report
.\.venv\Scripts\python.exe main.py --sanitize samples/gps_test.jpg
.\.venv\Scripts\python.exe main.py --compare samples/sample3.docx samples/modified.docx
```

Commands that analyze files ask for authorization before running.
