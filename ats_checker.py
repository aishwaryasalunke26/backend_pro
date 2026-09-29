# --------------------------------
# ATS Health Checker
# --------------------------------


def calculate_ats_score(
    profile,
    skills,
    education,
    projects,
    experience,
    certifications,
    achievements,
    resume_text
):
    """
    Calculate an ATS health score
    between 0 and 100.
    """

    score = 0

    breakdown = {}

    issues = []

    suggestions = []


    # --------------------------------
    # 1. Personal Information
    # Maximum: 15
    # --------------------------------

    profile_score = 0

    if profile.get("name"):
        profile_score += 3

    if profile.get("email"):
        profile_score += 4

    if profile.get("phone"):
        profile_score += 3

    if profile.get("linkedin"):
        profile_score += 2

    if profile.get("github"):
        profile_score += 2

    if profile.get("website"):
        profile_score += 1

    breakdown["personal_information"] = profile_score

    score += profile_score


    # --------------------------------
    # 2. Skills
    # Maximum: 20
    # --------------------------------

    skill_score = 0

    total_skills = 0

    for category in skills.values():

        if isinstance(category, list):
            total_skills += len(category)

    if total_skills >= 10:
        skill_score = 20

    elif total_skills >= 7:
        skill_score = 16

    elif total_skills >= 5:
        skill_score = 12

    elif total_skills >= 3:
        skill_score = 8

    elif total_skills >= 1:
        skill_score = 5

    breakdown["skills"] = skill_score

    score += skill_score


    # --------------------------------
    # 3. Education
    # Maximum: 15
    # --------------------------------

    education_score = 0

    if education.get("degrees"):
        education_score += 8

    if education.get("years"):
        education_score += 4

    if (
        education.get("cgpa")
        or education.get("percentage")
    ):
        education_score += 3

    breakdown["education"] = education_score

    score += education_score


    # --------------------------------
    # 4. Projects
    # Maximum: 15
    # --------------------------------

    project_score = 0

    project_count = projects.get(
        "count",
        0
    )

    if project_count >= 3:
        project_score = 15

    elif project_count == 2:
        project_score = 12

    elif project_count == 1:
        project_score = 7

    breakdown["projects"] = project_score

    score += project_score


    # --------------------------------
    # 5. Experience
    # Maximum: 15
    # --------------------------------

    experience_score = 0

    experience_count = experience.get(
        "count",
        0
    )

    if experience_count >= 2:
        experience_score = 15

    elif experience_count == 1:
        experience_score = 8

    breakdown["experience"] = experience_score

    score += experience_score


    # --------------------------------
    # 6. Certifications
    # Maximum: 5
    # --------------------------------

    certification_score = 0

    certification_count = certifications.get(
        "count",
        0
    )

    if certification_count >= 2:
        certification_score = 5

    elif certification_count == 1:
        certification_score = 3

    breakdown["certifications"] = certification_score

    score += certification_score


    # --------------------------------
    # 7. Achievements
    # Maximum: 5
    # --------------------------------

    achievement_score = 0

    achievement_count = achievements.get(
        "count",
        0
    )

    if achievement_count >= 2:
        achievement_score = 5

    elif achievement_count == 1:
        achievement_score = 3

    breakdown["achievements"] = achievement_score

    score += achievement_score


    # --------------------------------
    # 8. Resume Content
    # Maximum: 10
    # --------------------------------

    content_score = 0

    word_count = len(
        resume_text.split()
    )

    if word_count >= 400:
        content_score = 10

    elif word_count >= 300:
        content_score = 8

    elif word_count >= 200:
        content_score = 6

    elif word_count >= 100:
        content_score = 4

    else:
        content_score = 2

    breakdown["resume_content"] = content_score

    score += content_score


    # --------------------------------
    # ATS Issues
    # --------------------------------

    if not profile.get("phone"):
        issues.append(
            "Phone number is missing."
        )

        suggestions.append(
            "Add a professional phone number."
        )


    if not profile.get("linkedin"):
        issues.append(
            "LinkedIn profile is missing."
        )

        suggestions.append(
            "Add your LinkedIn profile URL."
        )


    if not profile.get("github"):
        issues.append(
            "GitHub profile is missing."
        )

        suggestions.append(
            "Add your GitHub profile URL."
        )


    if project_count == 0:
        issues.append(
            "No projects detected."
        )

        suggestions.append(
            "Add relevant technical projects."
        )


    if experience_count == 0:
        issues.append(
            "No work experience or internship detected."
        )

        suggestions.append(
            "Add internships, training, or relevant experience."
        )


    if total_skills < 5:
        issues.append(
            "Few technical skills detected."
        )

        suggestions.append(
            "Add relevant technical skills matching your target role."
        )


    if not education.get("cgpa") and not education.get(
        "percentage"
    ):
        issues.append(
            "CGPA or percentage is not detected."
        )

        suggestions.append(
            "Add CGPA or percentage if appropriate for your resume."
        )


    # --------------------------------
    # Final Score Safety
    # --------------------------------

    if score > 100:
        score = 100

    if score < 0:
        score = 0


    # --------------------------------
    # Health Label
    # --------------------------------

    if score >= 80:
        health = "Strong"

    elif score >= 60:
        health = "Good"

    elif score >= 40:
        health = "Needs Improvement"

    else:
        health = "Weak"


    # --------------------------------
    # Final Result
    # --------------------------------

    return {

        "ats_score": score,

        "health": health,

        "breakdown": breakdown,

        "issues": issues,

        "suggestions": suggestions
    }