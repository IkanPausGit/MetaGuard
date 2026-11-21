
from pathlib import Path
from extractor import (extract_image_metadata, extract_pdf_metadata, extract_docx_metadata)
from detector import detect_sensitive_metadata
from risk_analyzer import analyze_risk
from comparator import compare_metadata
from sanitizer import (sanitize_image, sanitize_pdf, sanitize_docx)
from reporter import generate_html_report
import argparse
import sys


def create_parser():
    parser = argparse.ArgumentParser(
        description=(
            "MetaGuard - Metadata Privacy Analysis "
            "and Sanitization Tool"
        ),
        epilog=(
            "Examples:\n"
            "  python main.py --scan samples/test.png\n"
            "  python main.py --scan samples/sample2.pdf --report\n"
            "  python main.py --sanitize samples/test.png\n"
            "  python main.py --compare samples/sample3.docx samples/modified.docx\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    actions = parser.add_mutually_exclusive_group()

    actions.add_argument(
        "--scan",
        metavar="FILE",
        help="Extract metadata and assess privacy risk"
    )

    actions.add_argument(
        "--sanitize",
        metavar="FILE",
        help="Create a sanitized copy of a file"
    )

    actions.add_argument(
        "--compare",
        nargs=2,
        metavar=("ORIGINAL", "MODIFIED"),
        help="Compare metadata between two files"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate an HTML report for --scan"
    )

    return parser



def validate_file(file_name, allow_output=False):
    project_dir = Path(__file__).resolve().parent

    samples_dir = (project_dir / "samples").resolve()
    output_dir = (project_dir / "output").resolve()

    file_path = Path(file_name).resolve()
    allowed_dirs = [samples_dir]
    if allow_output:
        allowed_dirs.append(output_dir)

    if not any(
        file_path.is_relative_to(directory)
        for directory in allowed_dirs
    ):
        raise ValueError(
            "Unauthorized file path. "
            "Only samples/ and permitted output/ files are allowed."
        )
    if not file_path.is_file():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )
    if file_path.suffix.lower() not in {
        ".jpg", ".jpeg", ".png", ".pdf", ".docx"
    }:
        raise ValueError("Unsupported file format.")
    return file_path




def run_cli(args):
    if args.report and not args.scan:
        raise ValueError("--report requires --scan.")


    if args.scan:
        file_path = validate_file(args.scan, allow_output=True)

        metadata = extract_by_type(file_path)
        findings = detect_sensitive_metadata(metadata)
        risk = analyze_risk(findings)

        print("\n--- METADATA RESULTS ---")
        for key, value in metadata.items():
            print(f"{key}: {value}")

        print("\n--- PRIVACY RISK ASSESSMENT ---")
        print(f"Risk Score: {risk['score']}/100")
        print(f"Risk Level: {risk['level']}")

        for recommendation in risk["recommendations"]:
            print(f" - {recommendation}")

        if args.report:
            path = generate_html_report(metadata, findings, risk)
            print(f"\nReport saved to: {path}")

    elif args.sanitize:
        file_path = validate_file(args.sanitize)

        extension = file_path.suffix.lower()

        if extension in {".jpg", ".jpeg", ".png"}:
            output_path = sanitize_image(file_path)
        elif extension == ".pdf":
            output_path = sanitize_pdf(file_path)
        elif extension == ".docx":
            output_path = sanitize_docx(file_path)

        before = analyze_risk(
            detect_sensitive_metadata(extract_by_type(file_path))
        )

        after = analyze_risk(
            detect_sensitive_metadata(extract_by_type(output_path))
        )

        print("\n--- SANITIZATION RESULT ---")
        print(f"Cleaned copy: {output_path}")
        print(f"Risk before: {before['score']}/100")
        print(f"Risk after: {after['score']}/100")

    elif args.compare:
        first = validate_file(args.compare[0], allow_output=True)
        second = validate_file(args.compare[1], allow_output=True)

        comparison = compare_metadata(
            extract_by_type(first),
            extract_by_type(second)
        )

        print("\n--- METADATA COMPARISON ---")
        for category, entries in comparison.items():
            print(f"\n{category.upper()} ({len(entries)}):")
            for key, value in entries.items():
                print(f" {key}: {value}")


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

def interactive_mode():
    print("================================")
    print("         MetaGuard v0.5")
    print("================================")
    print("For authorized local file analysis only.")
    print("Unauthorized access may violate Malaysia's")
    print("Computer Crimes Act 1997 (Act 563).")

    confirmation = input(
        "\nDo you own or have permission to analyze "
        "these files? (yes/no): "
    )

    if confirmation.strip().lower() != "yes":
        print("Authorization not confirmed. Exiting.")
        raise SystemExit(1)


    file_name = input(
        "\nEnter file name (e.g. test.png): "
    ).strip()

    file_path = Path("samples") / file_name

    # Only allow files directly inside samples/
    if (
        not file_name
        or Path(file_name).name != file_name
        or not file_path.is_file()
    ):
        print("Invalid file name or file not found in samples.")
        raise SystemExit(1)


    if not file_path.is_file():
        print(f"Test file not found: {file_path}")
        raise SystemExit(1)

    try:

        metadata = extract_by_type(file_path)

        print("\n--- METADATA RESULTS ---")

        for key, value in metadata.items():
            print(f"{key}: {value}")

        
        findings = detect_sensitive_metadata(metadata)

        print("\n--- PRIVACY FINDINGS ---")

        if findings:
            for finding in findings:
                print(
                    f"[!] {finding['category']}: "
                    f"{finding['field']}"
                )
        else:
            print("No predefined sensitive metadata fields detected.")


        risk_result = analyze_risk(findings)

        print("\n--- PRIVACY RISK ASSESSMENT ---")

        print(f"Risk Score: {risk_result['score']}/100")
        print(f"Risk Level: {risk_result['level']}")

        print("\nRisk Breakdown:")

        for detail in risk_result["details"]:
            print(
                f" - {detail['category']}: "
                f"+{detail['points']} points"
            )

        print("\nRecommendations:")

        if risk_result["recommendations"]:
            for recommendation in risk_result["recommendations"]:
                print(f" - {recommendation}")
        else:
            print(" - No predefined risk indicators detected.")

        
        compare_choice = input(
            "\nCompare with another file? (yes/no): "
        ).strip().lower()

        if compare_choice == "yes":
            second_name = input(
                "Enter second file name: "
            ).strip()

            second_path = Path("samples") / second_name

            if (
                not second_name
                or Path(second_name).name != second_name
                or not second_path.is_file()
            ):
                print("Invalid comparison file.")
            else:
                second_metadata = extract_by_type(second_path)
                
                try:
                    comparison = compare_metadata(
                        metadata,
                        second_metadata
                    )
                except ValueError as error:
                    print(f"\nComparison error: {error}")
                else:
                    print("\n--- METADATA COMPARISON ---")

                    for category in ["added", "removed", "changed", "unchanged"]:
                        results = comparison[category]

                        print(f"\n{category.upper()} ({len(results)}):")

                        if not results:
                            print(" None")
                        else:
                            for key, value in results.items():
                                if category == "changed":
                                    print(f" {key}:")
                                    print(f"   Before: {value['before']}")
                                    print(f"   After:  {value['after']}")
                                else:
                                    print(f" {key}: {value}")

        sanitize_choice = input(
            "\nSanitize this file? (yes/no): "
        ).strip().lower()

        if sanitize_choice == "yes":
            extension = file_path.suffix.lower()

            try:
                if extension in [".jpg", ".jpeg", ".png"]:
                    cleaned_path = sanitize_image(file_path)

                elif extension == ".pdf":
                    cleaned_path = sanitize_pdf(file_path)

                elif extension == ".docx":
                    cleaned_path = sanitize_docx(file_path)

                else:
                    raise ValueError(
                        "Sanitization is not supported for this format."
                    )

                # Extract the metadata of the cleaned file
                cleaned_metadata = extract_by_type(cleaned_path)

                cleaned_findings = detect_sensitive_metadata(
                    cleaned_metadata
                )

                cleaned_risk = analyze_risk(cleaned_findings)

                print("\n--- SANITIZATION RESULT ---")
                print(f"Original: {file_path}")
                print(f"Cleaned copy: {cleaned_path}")

                print(
                    f"Original sensitive fields: {len(findings)}"
                )
                print(
                    f"Remaining sensitive fields: {len(cleaned_findings)}"
                )

                print("\n--- RISK COMPARISON ---")
                print(f"Before: {risk_result['score']}/100")
                print(f"After: {cleaned_risk['score']}/100")

                if cleaned_findings:
                    print("\nRemaining findings:")
                    for finding in cleaned_findings:
                        print(
                            f" - {finding['field']}: "
                            f"{finding['category']}"
                        )

                print(
                    "\nNote: This checks detected metadata fields only."
                )

            except (OSError, ValueError) as error:
                print(f"\nSanitization failed: {error}")

        report_choice = input(
            "\nGenerate HTML security report? (yes/no): "
        ).strip().lower()

        if report_choice == "yes":
            report_path = generate_html_report(
                metadata,
                findings,
                risk_result
            )

            print("\n--- REPORT GENERATED ---")
            print(f"Report saved to: {report_path}")
            print("Open the HTML file in your browser.")


    except (OSError, ValueError) as error:
        print(f"Unable to analyze file: {error}")

    except KeyboardInterrupt:
        print("\nAnalysis cancelled.")
        raise SystemExit(130)
    
    pass



if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    try:
        if len(sys.argv) == 1:
            interactive_mode()
        else:
            print("================================")
            print("         MetaGuard CLI v0.5")
            print("================================")
            print(
                "For authorized analysis only. "
                "Unauthorized access may violate Malaysia's "
                "Computer Crimes Act 1997 (Act 563)."
            )

            authorization = input(
                "Confirm authorization (yes/no): "
            ).strip().lower()

            if authorization != "yes":
                print("Authorization not confirmed.")
                sys.exit(1)

            run_cli(args)

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(130)

    except (OSError, ValueError) as error:
        print(f"\nError: {error}")
        sys.exit(1)
