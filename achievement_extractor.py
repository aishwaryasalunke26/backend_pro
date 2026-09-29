import re


# --------------------------------
# Achievement Section Keywords
# --------------------------------

ACHIEVEMENT_SECTION_KEYWORDS = [
    "achievements",
    "achievement",
    "accomplishments",
    "accomplishment",
    "honors",
    "honours"
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
    "certifications",
    "interests",
    "hobbies",
    "references"
]


# --------------------------------
# Find Achievement Section
# --------------------------------

def extract_achievement_section(text):
    """
    Extract the Achievements section
    from the resume.
    """

    lines = text.splitlines()

    achievement_lines = []

    inside_achievements = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Start achievement section
        if lower_line in ACHIEVEMENT_SECTION_KEYWORDS:

            inside_achievements = True

            continue

        # Stop achievement section
        if (
            inside_achievements
            and lower_line in SECTION_END_KEYWORDS
        ):

            break

        if inside_achievements:

            achievement_lines.append(
                clean_line
            )

    return achievement_lines


# --------------------------------
# Clean Achievement
# --------------------------------

def clean_achievement_line(line):
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
# Extract Achievement Names
# --------------------------------

def extract_achievement_names(
    achievement_lines
):

    achievements = []

    for line in achievement_lines:

        clean_line = clean_achievement_line(
            line
        )

        if not clean_line:
            continue

        # Ignore page numbers
        if clean_line.isdigit():
            continue

        # Ignore section headings
        if clean_line.lower() in [
            "achievement",
            "achievements",
            "accomplishment",
            "accomplishments",
            "honors",
            "honours"
        ]:
            continue

        # Ignore URLs
        lower_line = clean_line.lower()

        if (
            "http://" in lower_line
            or "https://" in lower_line
            or "www." in lower_line
        ):
            continue

        # Ignore extremely long text
        if len(clean_line.split()) > 30:
            continue

        achievements.append(clean_line)

    return achievements


# --------------------------------
# Main Achievement Extraction
# --------------------------------

def extract_achievements(text):
    """
    Extract achievement information
    from resume.
    """

    achievement_section = (
        extract_achievement_section(text)
    )

    achievement_names = (
        extract_achievement_names(
            achievement_section
        )
    )

    return {
        "achievements_found":
            achievement_names,

        "count":
            len(achievement_names)
    }