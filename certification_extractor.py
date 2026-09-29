import re


# --------------------------------
# Certification Section Keywords
# --------------------------------

CERTIFICATION_SECTION_KEYWORDS = [
    "certifications",
    "certification",
    "certificates",
    "certification courses",
    "professional certifications"
]


# --------------------------------
# Section Ending Keywords
# --------------------------------

SECTION_END_KEYWORDS = [
    "experience",
    "work experience",
    "internship experience",
    "education",
    "projects",
    "skills",
    "technical skills",
    "achievements",
    "interests",
    "hobbies",
    "references"
]


# --------------------------------
# Find Certification Section
# --------------------------------

def extract_certification_section(text):
    """
    Extract the Certifications section
    from the resume.
    """

    lines = text.splitlines()

    certification_lines = []

    inside_certifications = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Start certification section
        if lower_line in CERTIFICATION_SECTION_KEYWORDS:

            inside_certifications = True

            continue

        # Stop certification section
        if (
            inside_certifications
            and lower_line in SECTION_END_KEYWORDS
        ):

            break

        if inside_certifications:

            certification_lines.append(
                clean_line
            )

    return certification_lines


# --------------------------------
# Clean Certification Name
# --------------------------------

def clean_certification_line(line):
    """
    Remove bullet symbols and
    unnecessary spaces.
    """

    line = re.sub(
        r"^[•\-*▪●]+\s*",
        "",
        line
    )

    return line.strip()


# --------------------------------
# Extract Certification Names
# --------------------------------

def extract_certification_names(
    certification_lines
):

    certifications = []

    for line in certification_lines:

        clean_line = clean_certification_line(
            line
        )

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Ignore page numbers
        if clean_line.isdigit():
            continue

        # Ignore common metadata
        if lower_line in [
            "certificate",
            "certification",
            "certifications",
            "course",
            "courses"
        ]:
            continue

        # Ignore URLs
        if (
            "http://" in lower_line
            or "https://" in lower_line
            or "www." in lower_line
        ):
            continue

        # Ignore extremely long descriptions
        if len(clean_line.split()) > 15:
            continue

        certifications.append(clean_line)

    return certifications


# --------------------------------
# Main Certification Extraction
# --------------------------------

def extract_certifications(text):
    """
    Extract certification information
    from resume.
    """

    certification_section = (
        extract_certification_section(text)
    )

    certification_names = (
        extract_certification_names(
            certification_section
        )
    )

    return {
        "certifications_found":
            certification_names,

        "count":
            len(certification_names)
    }