import re


# --------------------------------
# Experience Section Keywords
# --------------------------------

EXPERIENCE_SECTION_KEYWORDS = [
    "experience",
    "work experience",
    "internship experience",
    "professional experience",
    "employment experience",
    "internships"
]


# --------------------------------
# Section Ending Keywords
# --------------------------------

SECTION_END_KEYWORDS = [
    "education",
    "projects",
    "skills",
    "technical skills",
    "certifications",
    "achievements",
    "interests",
    "hobbies",
    "references"
]


# --------------------------------
# Find Experience Section
# --------------------------------

def extract_experience_section(text):
    """
    Extract the Experience section
    from the resume.
    """

    lines = text.splitlines()

    experience_lines = []

    inside_experience = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Start experience section
        if lower_line in EXPERIENCE_SECTION_KEYWORDS:

            inside_experience = True

            continue

        # Stop experience section
        if inside_experience and lower_line in SECTION_END_KEYWORDS:

            break

        if inside_experience:

            experience_lines.append(clean_line)

    return experience_lines


# --------------------------------
# Check Date / Duration
# --------------------------------

def is_duration(line):
    """
    Check whether a line contains
    an experience duration.
    """

    pattern = r"\b(19|20)\d{2}\b.*\b(19|20)\d{2}\b"

    if re.search(pattern, line):
        return True

    # Example:
    # Jan 2026 – Mar 2026
    # June 2025 - August 2025

    month_pattern = (
        r"(Jan|January|Feb|February|Mar|March|Apr|April|"
        r"May|Jun|June|Jul|July|Aug|August|Sep|September|"
        r"Oct|October|Nov|November|Dec|December)"
    )

    if re.search(
        month_pattern + r".*\d{4}",
        line,
        re.IGNORECASE
    ):
        return True

    return False


# --------------------------------
# Clean Description
# --------------------------------

def clean_description(line):
    """
    Remove bullet symbols.
    """

    return re.sub(
        r"^[•\-*▪●]+\s*",
        "",
        line
    ).strip()


# --------------------------------
# Extract Experiences
# --------------------------------

def extract_experience_details(experience_lines):

    experiences = []

    current_experience = None

    for line in experience_lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        # --------------------------------
        # Description bullet
        # --------------------------------

        if clean_line.startswith(
            ("•", "-", "*", "▪", "●")
        ):

            if current_experience:

                description = clean_description(
                    clean_line
                )

                current_experience[
                    "description"
                ].append(description)

            continue

        # --------------------------------
        # Duration
        # --------------------------------

        if is_duration(clean_line):

            if current_experience:

                current_experience[
                    "duration"
                ] = clean_line

            continue

        # --------------------------------
        # New experience
        # --------------------------------

        # If we already have a role/company,
        # a new non-bullet line after duration
        # usually represents the company.

        if current_experience is None:

            current_experience = {
                "role": clean_line,
                "duration": None,
                "company": None,
                "description": []
            }

            continue

        # --------------------------------
        # Company
        # --------------------------------

        if (
            current_experience["company"] is None
            and current_experience["duration"] is not None
        ):

            current_experience[
                "company"
            ] = clean_line

            continue

        # --------------------------------
        # New experience after company
        # --------------------------------

        if (
            current_experience["company"] is not None
        ):

            experiences.append(
                current_experience
            )

            current_experience = {
                "role": clean_line,
                "duration": None,
                "company": None,
                "description": []
            }

    # Add final experience
    if current_experience:

        experiences.append(
            current_experience
        )

    return experiences


# --------------------------------
# Main Experience Extraction
# --------------------------------

def extract_experience(text):
    """
    Extract complete internship
    and work experience information.
    """

    experience_section = extract_experience_section(
        text
    )

    experiences = extract_experience_details(
        experience_section
    )

    return {
        "experience_found": experiences,
        "count": len(experiences)
    }