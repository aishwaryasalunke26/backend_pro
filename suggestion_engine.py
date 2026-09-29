# --------------------------------
# Resume Suggestion Engine
# --------------------------------


def generate_suggestions(
    profile,
    skills,
    education,
    projects,
    experience,
    certifications,
    achievements,
    ats_result,
    keyword_result
):
    suggestions = []

    # --------------------------------
    # Personal Information
    # --------------------------------

    if not profile.get("phone"):
        suggestions.append(
            "Add your professional phone number."
        )

    if not profile.get("linkedin"):
        suggestions.append(
            "Add your LinkedIn profile URL."
        )

    if not profile.get("github"):
        suggestions.append(
            "Add your GitHub profile URL."
        )

    if not profile.get("website"):
        suggestions.append(
            "Consider adding a portfolio website if relevant."
        )

    # --------------------------------
    # Skills
    # --------------------------------

    total_skills = 0

    for category in skills.values():

        if isinstance(category, list):
            total_skills += len(category)

    if total_skills < 5:
        suggestions.append(
            "Add more relevant technical skills matching your target job role."
        )

    # --------------------------------
    # Education
    # --------------------------------

    if (
        not education.get("cgpa")
        and not education.get("percentage")
    ):
        suggestions.append(
            "Add CGPA or percentage if appropriate for your resume."
        )

    # --------------------------------
    # Projects
    # --------------------------------

    project_count = projects.get(
        "count",
        0
    )

    if project_count == 0:
        suggestions.append(
            "Add at least one relevant technical project."
        )

    elif project_count == 1:
        suggestions.append(
            "Consider adding another relevant technical project."
        )

    # --------------------------------
    # Experience
    # --------------------------------

    experience_count = experience.get(
        "count",
        0
    )

    if experience_count == 0:
        suggestions.append(
            "Add internships, training, or relevant practical experience."
        )

    # --------------------------------
    # Certifications
    # --------------------------------

    certification_count = certifications.get(
        "count",
        0
    )

    if certification_count == 0:
        suggestions.append(
            "Add relevant technical certifications if available."
        )

    # --------------------------------
    # Achievements
    # --------------------------------

    achievement_count = achievements.get(
        "count",
        0
    )

    if achievement_count == 0:
        suggestions.append(
            "Add relevant academic or technical achievements."
        )

    # --------------------------------
    # Keywords
    # --------------------------------

    unique_keywords = keyword_result.get(
        "total_unique_keywords",
        0
    )

    if unique_keywords < 5:
        suggestions.append(
            "Add more job-relevant technical keywords to improve keyword matching."
        )

    # --------------------------------
    # ATS Score
    # --------------------------------

    ats_score = ats_result.get(
        "ats_score",
        0
    )

    if ats_score < 60:
        suggestions.append(
            "Improve the overall resume structure and content to increase ATS compatibility."
        )

    elif ats_score < 80:
        suggestions.append(
            "Make additional improvements to strengthen your ATS score."
        )

    # --------------------------------
    # Remove Duplicate Suggestions
    # --------------------------------

    unique_suggestions = []

    for suggestion in suggestions:

        if suggestion not in unique_suggestions:
            unique_suggestions.append(
                suggestion
            )

    # --------------------------------
    # Final Result
    # --------------------------------

    return {
        "suggestions": unique_suggestions,
        "count": len(unique_suggestions)
    }