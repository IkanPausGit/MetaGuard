
RISK_WEIGHTS = {
    "Location information": 35,
    "Identity information": 20,
    "Device information": 10,
    "Software information": 10,
    "Timestamp information": 5
}

RECOMMENDATIONS = {
    "Location information": "Remove GPS metadata before sharing.",
    "Identity information": "Review author and editor names.",
    "Device information": "Remove unnecessary device details.",
    "Software information": "Review exposed software information.",
    "Timestamp information": "Review creation and modification dates."
}


def analyze_risk(findings):
    detected_categories = set()

    for finding in findings:
        detected_categories.add(finding["category"])

    total_score = 0
    risk_details = []
    recommendations = []

    for category in sorted(detected_categories):
        points = RISK_WEIGHTS.get(category, 0)
        total_score += points

        risk_details.append({
            "category": category,
            "points": points
        })

        if category in RECOMMENDATIONS:
            recommendations.append(RECOMMENDATIONS[category])

    total_score = min(total_score, 100)

    if total_score >= 60:
        risk_level = "HIGH"
    elif total_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "score": total_score,
        "level": risk_level,
        "details": risk_details,
        "recommendations": recommendations
    }
