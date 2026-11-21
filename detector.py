
# Metadata fields that may reveal information
SENSITIVE_FIELDS = {
    "Author": "Identity information",
    "/Author": "Identity information",
    "Last Modified By": "Identity information",
    "GPSInfo": "Location information",
    "GPSLatitude": "Location information",
    "GPSLongitude": "Location information",
    "Make": "Device information",
    "Model": "Device information",
    "Software": "Software information",
    "/Creator": "Software information",
    "/Producer": "Software information",
    "Created": "Timestamp information",
    "Modified": "Timestamp information",
    "/CreationDate": "Timestamp information",
    "/ModDate": "Timestamp information"
}



def detect_sensitive_metadata(metadata):
    findings = []

    for field, value in metadata.items():
        if field not in SENSITIVE_FIELDS:
            continue

        if value is None:
            continue

        cleaned_value = str(value).strip()

        if not cleaned_value or cleaned_value.lower() == "none":
            continue

        findings.append({
            "field": field,
            "category": SENSITIVE_FIELDS[field],
            "value": value
        })

    return findings

