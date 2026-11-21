from pathlib import Path

from detector import detect_sensitive_metadata
from extractor import extract_docx_metadata, extract_image_metadata, extract_pdf_metadata
from risk_analyzer import analyze_risk
from reporter import generate_html_report
from sanitizer import sanitize_docx, sanitize_image, sanitize_pdf
from comparator import compare_metadata


SAMPLES_DIR = Path(__file__).resolve().parent / "samples"


def read_sample(prompt):
    file_name = input(prompt).strip()
    file_path = (SAMPLES_DIR / file_name).resolve()
    if not file_name or Path(file_name).name != file_name or file_path.parent != SAMPLES_DIR:
        raise ValueError("Enter the name of a file in samples/.")
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found in samples/: {file_name}")
    return file_path


def print_scan(metadata, findings, risk):
    print("\n--- METADATA RESULTS ---")
    for field, value in metadata.items():
        print(f"{field}: {value}")

    print("\n--- PRIVACY FINDINGS ---")
    for finding in findings:
        print(f"[!] {finding['category']}: {finding['field']}")
    if not findings:
        print("No predefined sensitive metadata fields detected.")

    print("\n--- PRIVACY RISK ASSESSMENT ---")
    print(f"Risk Score: {risk['score']}/100")
    print(f"Risk Level: {risk['level']}")
    for detail in risk["details"]:
        print(f" - {detail['category']}: +{detail['points']} points")
    for recommendation in risk["recommendations"]:
        print(f" - {recommendation}")



def extract_by_type(file_path):
    extension = file_path.suffix.lower()

    if extension in [".jpg", ".jpeg", ".png"]:
        return extract_image_metadata(file_path)

    elif extension == ".pdf":
        return extract_pdf_metadata(file_path)

    elif extension == ".docx":
        return extract_docx_metadata(file_path)

    else:
        raise ValueError("Unsupported file format.")


def sanitize_and_check(file_path, original_risk):
    extension = file_path.suffix.lower()
    if extension in {".jpg", ".jpeg", ".png"}:
        cleaned_path = sanitize_image(file_path)
    elif extension == ".pdf":
        cleaned_path = sanitize_pdf(file_path)
    elif extension == ".docx":
        cleaned_path = sanitize_docx(file_path)

    cleaned_findings = detect_sensitive_metadata(extract_by_type(cleaned_path))
    cleaned_risk = analyze_risk(cleaned_findings)

    print("\n--- SANITIZATION RESULT ---")
    print(f"Cleaned copy: {cleaned_path}")
    print(f"Risk before: {original_risk['score']}/100")
    print(f"Risk after: {cleaned_risk['score']}/100")
    print(f"Remaining sensitive fields: {len(cleaned_findings)}")
    for finding in cleaned_findings:
        print(f" - {finding['field']}: {finding['category']}")


def print_comparison(metadata, second_file):
    comparison = compare_metadata(metadata, extract_by_type(second_file))
    print("\n--- METADATA COMPARISON ---")
    for category, entries in comparison.items():
        print(f"\n{category.upper()} ({len(entries)}):")
        for field, value in entries.items():
            if category == "changed":
                print(f" {field}:")
                print(f"   Before: {value['before']}")
                print(f"   After:  {value['after']}")
            else:
                print(f" {field}: {value}")


def main():
    print("MetaGuard v0.4")
    confirmation = input("Do you own or have permission to analyze these files? (yes/no): ")
    if confirmation.strip().lower() != "yes":
        print("Authorization not confirmed. Exiting.")
        return 1

    file_path = read_sample("\nEnter file name (e.g. gps_test.jpg): ")
    metadata = extract_by_type(file_path)
    findings = detect_sensitive_metadata(metadata)
    risk = analyze_risk(findings)
    print_scan(metadata, findings, risk)

    if input("\nCompare with another file? (yes/no): ").strip().lower() == "yes":
        try:
            second_file = read_sample("Enter second file name: ")
            print_comparison(metadata, second_file)
        except (OSError, ValueError) as error:
            print(f"Comparison error: {error}")

    if input("\nSanitize this file? (yes/no): ").strip().lower() == "yes":
        try:
            sanitize_and_check(file_path, risk)
        except (OSError, ValueError) as error:
            print(f"Sanitization failed: {error}")

    if input("\nGenerate HTML security report? (yes/no): ").strip().lower() == "yes":
        report_path = generate_html_report(metadata, findings, risk)
        print(f"Report saved to: {report_path}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)
    except (EOFError, KeyboardInterrupt):
        print("\nAnalysis cancelled.")
        raise SystemExit(130)
