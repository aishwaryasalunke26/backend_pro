import re


def extract_email(text):
    """Extract email address from resume."""

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_phone(text):
    """Extract phone number from resume."""

    patterns = [
        r"\+91[-\s]?\d{10}",
        r"\+91[-\s]?\d{5}[-\s]?\d{5}",
        r"\b\d{10}\b",
        r"\b\d{5}[-\s]\d{5}\b"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group(0)

    return None


def extract_linkedin(text):
    """Extract LinkedIn profile URL."""

    pattern = r"(https?://)?(www\.)?linkedin\.com/[A-Za-z0-9_./-]+"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(0)

    return None


def extract_github(text):
    """Extract GitHub profile URL."""

    pattern = r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_.-]+"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(0)

    return None


def extract_website(text):
    """Extract personal website if available."""

    pattern = r"https?://[A-Za-z0-9./_-]+\.[A-Za-z]{2,}"

    matches = re.findall(
        pattern,
        text,
        re.IGNORECASE
    )

    for url in matches:

        if "linkedin.com" not in url.lower() \
                and "github.com" not in url.lower():

            return url

    return None


def extract_name(text):
    """
    Try to identify the candidate name.

    Usually the name appears near the beginning
    of the resume.
    """

    lines = text.splitlines()

    for line in lines[:10]:

        line = line.strip()

        if not line:
            continue

        # Ignore lines that look like contact information
        if "@" in line:
            continue

        if any(
            keyword in line.lower()
            for keyword in [
                "resume",
                "curriculum vitae",
                "cv",
                "objective",
                "profile",
                "phone",
                "email",
                "linkedin",
                "github"
            ]
        ):
            continue

        # Avoid very long sentences
        if len(line.split()) > 5:
            continue

        # Name usually contains letters and spaces
        if re.fullmatch(
            r"[A-Za-z][A-Za-z .'-]*",
            line
        ):

            return line

    return None


def extract_profile(text):
    """Extract complete personal information."""

    profile = {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "linkedin": extract_linkedin(text),

        "github": extract_github(text),

        "website": extract_website(text)
    }

    return profile