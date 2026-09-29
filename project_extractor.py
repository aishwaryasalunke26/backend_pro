import re


# --------------------------------
# Project Section Keywords
# --------------------------------

PROJECT_SECTION_KEYWORDS = [
    "projects",
    "academic projects",
    "academic project",
    "personal projects",
    "personal project",
    "key projects",
    "major projects"
]


# --------------------------------
# Section Ending Keywords
# --------------------------------

SECTION_END_KEYWORDS = [
    "experience",
    "work experience",
    "internship experience",
    "education",
    "skills",
    "technical skills",
    "certifications",
    "achievements",
    "internships",
    "interests",
    "hobbies",
    "references"
]


# --------------------------------
# Find Project Section
# --------------------------------

def extract_project_section(text):
    """
    Extract the Projects section
    from the resume.
    """

    lines = text.splitlines()

    project_lines = []

    inside_projects = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Start project section
        if any(
            keyword == lower_line
            for keyword in PROJECT_SECTION_KEYWORDS
        ):

            inside_projects = True

            continue

        # Stop project section
        if inside_projects and any(
            keyword == lower_line
            for keyword in SECTION_END_KEYWORDS
        ):

            break

        if inside_projects:

            project_lines.append(clean_line)

    return project_lines


# --------------------------------
# Clean Project Line
# --------------------------------

def clean_project_line(line):
    """
    Remove unnecessary symbols
    from project names.
    """

    line = re.sub(
        r"^[•\-*▪●]+\s*",
        "",
        line
    )

    return line.strip()


# --------------------------------
# Extract Project Names
# --------------------------------

def extract_project_names(project_lines):
    """
    Identify actual project title lines.
    Ignore project descriptions and links.
    """

    projects = []

    for line in project_lines:

        clean_line = clean_project_line(line)

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # --------------------------------
        # Ignore links and metadata
        # --------------------------------

        if lower_line in [
            "github",
            "live demo",
            "demo",
            "repository"
        ]:
            continue

        # --------------------------------
        # Ignore bullet descriptions
        # --------------------------------

        if line.startswith(
            ("•", "-", "*", "▪", "●")
        ):
            continue

        # --------------------------------
        # Ignore common description lines
        # --------------------------------

        if lower_line.startswith(
            (
                "developed",
                "implemented",
                "built",
                "designed",
                "created",
                "integrated",
                "worked",
                "used",
                "responsible",
                "technologies",
                "technology",
                "tools used",
                "description",
                "responsibilities"
            )
        ):
            continue

        # --------------------------------
        # Ignore very long sentences
        # --------------------------------

        if len(clean_line.split()) > 10:
            continue

        # --------------------------------
        # Add project title
        # --------------------------------

        projects.append(clean_line)

    return projects

# --------------------------------
# Main Project Extraction
# --------------------------------

def extract_projects(text):
    """
    Extract project information
    from resume text.
    """

    project_section = extract_project_section(text)

    project_names = extract_project_names(
        project_section
    )

    return {

        "projects_found": project_names,

        "count": len(project_names)
    }