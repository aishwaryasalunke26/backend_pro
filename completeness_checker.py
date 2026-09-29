# --------------------------------
# Resume Completeness Checker
# --------------------------------


def check_completeness(
    profile,
    skills,
    education,
    projects,
    experience,
    certifications,
    achievements
):

    sections = {}

    # --------------------------------
    # Personal Information
    # --------------------------------

    sections["personal_information"] = bool(
        profile.get("name")
        and profile.get("email")
    )

    # --------------------------------
    # Skills
    # --------------------------------

    total_skills = 0

    for category in skills.values():

        if isinstance(category, list):
            total_skills += len(category)

    sections["skills"] = total_skills > 0

    # --------------------------------
    # Education
    # --------------------------------

    sections["education"] = bool(
        education.get("degrees")
    )

    # --------------------------------
    # Projects
    # --------------------------------

    sections["projects"] = (
        projects.get("count", 0) > 0
    )

    # --------------------------------
    # Experience
    # --------------------------------

    sections["experience"] = (
        experience.get("count", 0) > 0
    )

    # --------------------------------
    # Certifications
    # --------------------------------

    sections["certifications"] = (
        certifications.get("count", 0) > 0
    )

    # --------------------------------
    # Achievements
    # --------------------------------

    sections["achievements"] = (
        achievements.get("count", 0) > 0
    )

    # --------------------------------
    # Calculate Completeness
    # --------------------------------

    total_sections = len(sections)

    completed_sections = sum(
        1
        for value in sections.values()
        if value
    )

    missing_sections = total_sections - completed_sections

    completeness_percentage = round(
        (completed_sections / total_sections) * 100
    )

    # --------------------------------
    # Missing Section Names
    # --------------------------------

    missing = []

    for section, present in sections.items():

        if not present:
            missing.append(section)

    # --------------------------------
    # Final Result
    # --------------------------------

    return {

        "completeness_percentage":
            completeness_percentage,

        "total_sections":
            total_sections,

        "completed_sections":
            completed_sections,

        "missing_sections":
            missing_sections,

        "missing_section_names":
            missing,

        "section_status":
            sections
    }