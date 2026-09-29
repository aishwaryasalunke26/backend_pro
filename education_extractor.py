import re


# --------------------------------
# Degree Keywords
# --------------------------------

DEGREE_KEYWORDS = [
    "B.E",
    "BE",
    "B.Tech",
    "BTech",
    "Bachelor of Engineering",
    "Bachelor of Technology",
    "M.E",
    "ME",
    "M.Tech",
    "MTech",
    "Master of Engineering",
    "Master of Technology",
    "B.Sc",
    "BSc",
    "Bachelor of Science",
    "M.Sc",
    "MSc",
    "Master of Science",
    "BCA",
    "Bachelor of Computer Applications",
    "MCA",
    "Master of Computer Applications",
    "BBA",
    "MBA",
    "PhD"
]


# --------------------------------
# Extract Degree
# --------------------------------

def extract_degree(text):
    """
    Extract degree information from resume.
    """

    found_degrees = []

    for degree in DEGREE_KEYWORDS:

        pattern = r"(?<!\w)" + re.escape(degree) + r"(?!\w)"

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found_degrees.append(degree)

    return found_degrees


# --------------------------------
# Extract CGPA
# --------------------------------

def extract_cgpa(text):
    """
    Extract CGPA from resume.
    """

    patterns = [
        r"CGPA\s*[:\-]?\s*(\d+(?:\.\d+)?)",
        r"CGPA\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*/\s*10",
        r"(\d+(?:\.\d+)?)\s*/\s*10\s*CGPA"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return None


# --------------------------------
# Extract Percentage
# --------------------------------

def extract_percentage(text):
    """
    Extract percentage from resume.
    """

    patterns = [
        r"Percentage\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*%",
        r"(\d+(?:\.\d+)?)\s*%"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return None


# --------------------------------
# Extract Passing Year
# --------------------------------

def extract_year(text):
    """
    Extract education year.
    """

    # Look for years between 2000 and 2035
    years = re.findall(
        r"\b(20\d{2})\b",
        text
    )

    if years:

        return years

    return []


# --------------------------------
# Extract Education Section
# --------------------------------

def extract_education_section(text):
    """
    Try to identify the Education section
    from the resume.
    """

    lines = text.splitlines()

    education_lines = []

    inside_education = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Start of education section
        if any(
            keyword in lower_line
            for keyword in [
                "education",
                "academic qualification",
                "academic qualifications",
                "educational qualification",
                "educational qualifications"
            ]
        ):

            inside_education = True

            continue

        # Stop when another major section starts
        if inside_education and any(
            keyword in lower_line
            for keyword in [
                "experience",
                "work experience",
                "projects",
                "skills",
                "certifications",
                "achievements",
                "internships",
                "interests",
                "hobbies",
                "references"
            ]
        ):

            break

        if inside_education:

            education_lines.append(clean_line)

    return education_lines


# --------------------------------
# Main Education Extraction
# --------------------------------

def extract_education(text):
    """
    Extract complete education information.
    """

    education_section = extract_education_section(text)

    education_text = "\n".join(
        education_section
    )

    # If an Education heading was not found,
    # use the complete resume text.
    if not education_text.strip():

        education_text = text

    education = {

        "degrees":
            extract_degree(
                education_text
            ),

        "cgpa":
            extract_cgpa(
                education_text
            ),

        "percentage":
            extract_percentage(
                education_text
            ),

        "years":
            extract_year(
                education_text
            )
    }

    return education