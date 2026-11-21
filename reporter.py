
from pathlib import Path
from datetime import datetime
from html import escape


def generate_html_report(metadata, findings, risk_result):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    file_name = f"metaguard_report_{timestamp}.html"
    report_path = output_dir / file_name

    score = risk_result["score"]
    level = risk_result["level"]

    # Decide which color represents the risk level
    risk_colors = {
        "LOW": "#28a745",
        "MEDIUM": "#ffc107",
        "HIGH": "#dc3545"
    }

    risk_color = risk_colors.get(level, "#6c757d")

    def safe(value):
        return escape(str(value), quote=True)

    metadata_rows = ""
    for key, value in metadata.items():
        metadata_rows += (
            f"<tr><td>{safe(key)}</td>"
            f"<td>{safe(value)}</td></tr>"
        )

    findings_rows = ""
    for finding in findings:
        findings_rows += (
            f"<tr><td>{safe(finding['field'])}</td>"
            f"<td>{safe(finding['category'])}</td></tr>"
        )

    if not findings_rows:
        findings_rows = (
            "<tr><td colspan='2'>"
            "No predefined sensitive fields detected."
            "</td></tr>"
        )

    recommendation_items = ""
    for recommendation in risk_result["recommendations"]:
        recommendation_items += f"<li>{safe(recommendation)}</li>"

    if not recommendation_items:
        recommendation_items = "<li>No predefined recommendations.</li>"

    analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MetaGuard Security Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f9;
            color: #333;
            margin: 40px;
        }}
        .container {{
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
        }}
        h1 {{
            color: #17365d;
        }}
        h2 {{
            margin-top: 30px;
            color: #17365d;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
            overflow-wrap: anywhere;
        }}
        th {{
            background: #17365d;
            color: white;
        }}
        .risk {{
            padding: 15px;
            border-left: 6px solid {risk_color};
            background: #f8f9fa;
        }}
        li {{
            margin-bottom: 8px;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>MetaGuard Security Report</h1>
    <p>Automated Metadata Privacy Assessment</p>
    <p><strong>Analysis Date:</strong> {safe(analysis_time)}</p>

    <h2>1. Metadata Information</h2>
    <table>
        <tr><th>Field</th><th>Value</th></tr>
        {metadata_rows}
    </table>

    <h2>2. Sensitive Metadata Findings</h2>
    <table>
        <tr><th>Field</th><th>Category</th></tr>
        {findings_rows}
    </table>

    <h2>3. Privacy Risk Assessment</h2>
    <div class="risk">
        <h3>Risk Score: {score}/100</h3>
        <h3>Risk Level: {safe(level)}</h3>
    </div>

    <h2>4. Security Recommendations</h2>
    <ul>
        {recommendation_items}
    </ul>

    <h2>5. Assessment Limitations</h2>
    <p>
        This report identifies predefined metadata privacy
        indicators. Risk scores are illustrative, not proof
        of a security vulnerability. Undetected metadata
        or sensitive document content may still exist.
    </p>

    <hr>
    <p>Generated locally by MetaGuard.</p>
</div>
</body>
</html>
"""

    report_path.write_text(html_content, encoding="utf-8")

    return report_path
