"""
ATS Scorer Module - Scores CV based on ATS compatibility rules
"""

import re
from typing import List, Dict, Tuple


# ─── Section Detection Patterns ───────────────────────────────────────────────
SECTION_PATTERNS = {
    "Summary/Objective": [
        r"(?i)\b(summary|objective|professional\s+summary|career\s+objective|profile)\b",
    ],
    "Work Experience": [
        r"(?i)\b(work\s+experience|experience|employment\s+history|professional\s+experience|work\s+history)\b",
    ],
    "Education": [
        r"(?i)\b(education|academic|qualifications|degrees?|certifications?)\b",
    ],
    "Skills": [
        r"(?i)\b(skills|technical\s+skills|core\s+competencies|competencies|expertise|proficiencies)\b",
    ],
    "Contact Information": [
        r"(?i)\b(contact|contact\s+info|personal\s+details)\b",
    ],
}

# ─── Banking / Finance Keywords ───────────────────────────────────────────────
BANKING_KEYWORDS = [
    "banking",
    "finance",
    "financial",
    "investment",
    "risk management",
    "compliance",
    "regulatory",
    "audit",
    "accounting",
    "financial analysis",
    "budgeting",
    "forecasting",
    "treasury",
    "credit analysis",
    "loan",
    "portfolio",
    "asset management",
    "wealth management",
    "private banking",
    "corporate banking",
    "retail banking",
    "capital markets",
    "securities",
    "derivatives",
    "fixed income",
    "equity",
    "bonds",
    "mutual funds",
    "financial modeling",
    "valuation",
    "due diligence",
    "mergers",
    "acquisitions",
    "ipo",
    "financial reporting",
    "gaap",
    "ifrs",
    "anti-money laundering",
    "aml",
    "kyc",
    "know your customer",
    "basel",
    "liquidity",
    "solvency",
    "credit risk",
    "market risk",
    "operational risk",
    "stress testing",
    "scenario analysis",
]

CERTIFICATIONS = [
    "cfa",
    "cma",
    "cpa",
    "acca",
    "frm",
    "caia",
    "cfp",
    "cfa level",
    "cma level",
    "series 7",
    "series 63",
    "series 66",
    "chartered financial analyst",
    "certified management accountant",
    "certified public accountant",
    "financial risk manager",
]

ACTION_VERBS = [
    "managed",
    "led",
    "developed",
    "implemented",
    "achieved",
    "increased",
    "reduced",
    "optimized",
    "streamlined",
    "analyzed",
    "coordinated",
    "established",
    "negotiated",
    "supervised",
    "orchestrated",
    "delivered",
    "transformed",
    "spearheaded",
    "pioneered",
    "generated",
    "maximized",
    "administered",
    "directed",
    "executed",
    "facilitated",
]

WEAK_PHRASES = [
    "responsible for",
    "duties included",
    "helped with",
    "assisted in",
    "worked on",
    "tasked with",
    "in charge of",
]


def check_readability(parsed_cv: dict) -> Tuple[int, List[str]]:
    """
    Score readability (25 points max).
    Checks: text extraction, standard fonts, no excessive images/tables.
    """
    score = 0
    tips = []

    if not parsed_cv["is_readable"]:
        tips.append(
            "CRITICAL: CV text could not be extracted. Use a text-based PDF or DOCX, not a scanned image."
        )
        return 0, tips

    text = parsed_cv["text"]
    word_count = len(text.split())

    # Text length check (0-10 points)
    if word_count < 50:
        tips.append(
            "CV has very little text content. Ensure your CV has sufficient detail."
        )
        score += 3
    elif word_count < 150:
        tips.append(
            "CV is quite short. Consider adding more detail to your experience and skills."
        )
        score += 6
    elif word_count < 500:
        score += 8
    else:
        score += 10

    # Tables check (0-8 points)
    if parsed_cv.get("has_tables"):
        tips.append(
            "Tables detected in CV. ATS systems may not parse tables correctly. Consider converting tables to plain text lists."
        )
        score += 2
    else:
        score += 8

    # Images check (0-7 points)
    if parsed_cv.get("has_images"):
        tips.append(
            "Images detected. Remove images, icons, and graphics as ATS cannot read them."
        )
        score += 2
    else:
        score += 7

    return min(score, 25), tips


def check_sections(text: str) -> Tuple[int, List[str], Dict[str, bool]]:
    """
    Score section presence (25 points max).
    Checks for standard section headings.
    """
    score = 0
    tips = []
    found_sections = {}

    points_per_section = 5  # 5 sections x 5 = 25

    for section_name, patterns in SECTION_PATTERNS.items():
        found = False
        for pattern in patterns:
            if re.search(pattern, text):
                found = True
                break
        found_sections[section_name] = found
        if found:
            score += points_per_section
        else:
            if section_name == "Summary/Objective":
                tips.append(
                    "Missing 'Summary' or 'Objective' section. Add a 2-3 line professional summary at the top."
                )
            elif section_name == "Work Experience":
                tips.append(
                    "Missing 'Work Experience' section. Use standard heading like 'Work Experience' or 'Professional Experience'."
                )
            elif section_name == "Education":
                tips.append(
                    "Missing 'Education' section. Add your educational background with a clear heading."
                )
            elif section_name == "Skills":
                tips.append(
                    "Missing 'Skills' section. Add a dedicated skills section listing your key competencies."
                )
            elif section_name == "Contact Information":
                tips.append(
                    "Contact section heading not detected. Ensure your name, email, and phone are clearly at the top."
                )

    return min(score, 25), tips, found_sections


def check_keywords(text: str, job_description: str = "") -> Tuple[int, List[str], Dict]:
    """
    Score keyword match (30 points max).
    If job description provided, compare against it. Otherwise check banking keywords.
    """
    score = 0
    tips = []
    text_lower = text.lower()

    keyword_analysis = {
        "found_banking_keywords": [],
        "missing_banking_keywords": [],
        "found_certifications": [],
        "missing_certifications": [],
        "found_action_verbs": [],
        "weak_phrases_found": [],
        "jd_match_percentage": 0,
        "jd_matched_keywords": [],
        "jd_missing_keywords": [],
    }

    if job_description and job_description.strip():
        # Extract keywords from job description
        jd_lower = job_description.lower()
        jd_words = set(re.findall(r"\b[a-z][a-z\s]{2,}\b", jd_lower))
        jd_words = {w.strip() for w in jd_words if len(w.strip()) > 3}

        # Check which JD keywords appear in CV
        matched = []
        missing = []
        for kw in jd_words:
            if kw in text_lower:
                matched.append(kw)
            # Only flag important keywords (longer ones are more specific)
            elif len(kw) > 5:
                missing.append(kw)

        keyword_analysis["jd_matched_keywords"] = matched[:20]
        keyword_analysis["jd_missing_keywords"] = missing[:20]

        if len(matched) + len(missing) > 0:
            match_pct = len(matched) / (len(matched) + len(missing)) * 100
            keyword_analysis["jd_match_percentage"] = round(match_pct, 1)
            score = int(30 * match_pct / 100)
        else:
            score = 15  # neutral if can't determine

        if match_pct < 40:
            tips.append(
                f"Low keyword match with job description ({match_pct:.0f}%). Add more relevant keywords from the job posting."
            )
        elif match_pct < 70:
            tips.append(
                f"Moderate keyword match ({match_pct:.0f}%). Consider adding a few more keywords from the job description."
            )
    else:
        # Check general banking keywords
        found_kw = [kw for kw in BANKING_KEYWORDS if kw in text_lower]
        keyword_analysis["found_banking_keywords"] = found_kw

        # Score based on keyword density (0-15 points for general keywords)
        if len(found_kw) == 0:
            tips.append(
                "No banking/finance keywords detected. Add industry-relevant terms to your CV."
            )
            score += 3
        elif len(found_kw) < 5:
            tips.append(
                "Few banking keywords found. Enrich your CV with more industry-specific terminology."
            )
            score += 8
        elif len(found_kw) < 10:
            score += 12
        else:
            score += 15

        # Check certifications (0-10 points)
        found_certs = [c for c in CERTIFICATIONS if c in text_lower]
        keyword_analysis["found_certifications"] = found_certs

        if found_certs:
            score += 10
        else:
            tips.append(
                "No financial certifications (CFA, CMA, CPA, etc.) detected. Consider adding relevant certifications."
            )
            score += 2

        # Check for action verbs vs weak phrases
        found_verbs = [v for v in ACTION_VERBS if v in text_lower]
        found_weak = [w for w in WEAK_PHRASES if w in text_lower]
        keyword_analysis["found_action_verbs"] = found_verbs
        keyword_analysis["weak_phrases_found"] = found_weak

        if found_weak:
            tips.append(
                f"Weak phrases detected: {', '.join(found_weak[:3])}. Replace with strong action verbs like 'Managed', 'Developed', 'Achieved'."
            )

    return min(score, 30), tips, keyword_analysis


def check_contact_info(text: str) -> Tuple[int, List[str]]:
    """
    Score contact information (20 points max).
    """
    score = 0
    tips = []

    # Email check (0-7 points)
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    if re.search(email_pattern, text):
        score += 7
    else:
        tips.append(
            "No email address found. Add a professional email address to your CV."
        )

    # Phone check (0-7 points)
    phone_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
    if re.search(phone_pattern, text):
        score += 7
    else:
        tips.append("No phone number found. Add your contact number to your CV.")

    # LinkedIn check (0-6 points)
    linkedin_pattern = r"(?:linkedin\.com/in/|linkedin\s*:)"
    if re.search(linkedin_pattern, text, re.IGNORECASE):
        score += 6
    else:
        tips.append(
            "No LinkedIn profile link found. Add your LinkedIn URL to enhance your professional presence."
        )

    return min(score, 20), tips


def calculate_ats_score(parsed_cv: dict, job_description: str = "") -> Dict:
    """
    Calculate full ATS score and return detailed results.
    """
    text = parsed_cv["text"]

    # Calculate each section
    readability_score, readability_tips = check_readability(parsed_cv)
    sections_score, sections_tips, found_sections = check_sections(text)
    keywords_score, keywords_tips, keyword_analysis = check_keywords(
        text, job_description
    )
    contact_score, contact_tips = check_contact_info(text)

    # Total score
    total_score = readability_score + sections_score + keywords_score + contact_score

    # Determine score level
    if total_score >= 80:
        level = "Excellent"
        color = "#22C55E"  # green
    elif total_score >= 55:
        level = "Good"
        color = "#F59E0B"  # orange
    elif total_score >= 35:
        level = "Needs Improvement"
        color = "#F97316"  # dark orange
    else:
        level = "Poor"
        color = "#EF4444"  # red

    # Compile all tips
    all_tips = []
    if readability_tips:
        all_tips.extend([("Readability", t) for t in readability_tips])
    if sections_tips:
        all_tips.extend([("Sections", t) for t in sections_tips])
    if keywords_tips:
        all_tips.extend([("Keywords", t) for t in keywords_tips])
    if contact_tips:
        all_tips.extend([("Contact Info", t) for t in contact_tips])

    return {
        "total_score": total_score,
        "level": level,
        "color": color,
        "breakdown": {
            "readability": {
                "score": readability_score,
                "max": 25,
                "tips": readability_tips,
            },
            "sections": {
                "score": sections_score,
                "max": 25,
                "tips": sections_tips,
                "found": found_sections,
            },
            "keywords": {
                "score": keywords_score,
                "max": 30,
                "tips": keywords_tips,
                "analysis": keyword_analysis,
            },
            "contact": {"score": contact_score, "max": 20, "tips": contact_tips},
        },
        "all_tips": all_tips,
        "word_count": len(text.split()),
        "page_count": parsed_cv.get("page_count", 0),
    }
