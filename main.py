from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

from resume_parser import extract_text
from profile_extractor import extract_profile
from skill_extractor import extract_skills
from education_extractor import extract_education
from project_extractor import extract_projects
from experience_extractor import extract_experience
from certification_extractor import extract_certifications
from achievement_extractor import extract_achievements
from ats_checker import calculate_ats_score
from keyword_analyzer import analyze_keywords
from suggestion_engine import generate_suggestions
from completeness_checker import check_completeness
from database import get_connection


app = FastAPI(
    title="CodePilot Module 2",
    description="AI Resume Parsing, Skill Extraction & ATS Health Check",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder
UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "status": "success",
        "message": "CodePilot Module 2 is running"
    }


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    # --------------------------------
    # 1. Get file extension
    # --------------------------------

    extension = os.path.splitext(
        file.filename
    )[1].lower()


    # --------------------------------
    # 2. Check file type
    # --------------------------------

    if extension not in [".pdf", ".docx"]:

        return {
            "status": "error",
            "message": "Only PDF and DOCX files are allowed."
        }


    # --------------------------------
    # 3. Create unique filename
    # --------------------------------

    unique_name = (
        str(uuid.uuid4())
        + extension
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )


    # --------------------------------
    # 4. Read uploaded file
    # --------------------------------

    content = await file.read()


    # --------------------------------
    # 5. Save uploaded file
    # --------------------------------

    with open(
        file_path,
        "wb"
    ) as output_file:

        output_file.write(content)


    # --------------------------------
    # 6. Extract resume text
    # --------------------------------

    try:

        text = extract_text(
            file_path,
            extension
        )

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }


    # --------------------------------
    # 7. Check extracted text
    # --------------------------------

    if not text.strip():

        return {
            "status": "error",
            "message": "No readable text was found in the resume."
        }


    # --------------------------------
    # 8. Extract personal information
    # --------------------------------

    profile = extract_profile(text)


    # --------------------------------
    # 9. Extract technical skills
    # --------------------------------

    skills = extract_skills(text)


    # --------------------------------
    # 10. Extract education
    # --------------------------------

    education = extract_education(text)


    # --------------------------------
    # 11. Extract projects
    # --------------------------------

    projects = extract_projects(text)


    # --------------------------------
    # 12. Extract experience
    # --------------------------------

    experience = extract_experience(text)


    # --------------------------------
    # 13. Extract certifications
    # --------------------------------

    certifications = extract_certifications(text)


    # --------------------------------
    # 14. Extract achievements
    # --------------------------------

    achievements = extract_achievements(text)


    # --------------------------------
    # 15. Calculate ATS Health Score
    # --------------------------------

    ats_result = calculate_ats_score(
        profile,
        skills,
        education,
        projects,
        experience,
        certifications,
        achievements,
        text
    )


    # --------------------------------
    # 16. Analyze Resume Keywords
    # --------------------------------

    keyword_result = analyze_keywords(text)


    # --------------------------------
    # 17. Generate Suggestions
    # --------------------------------

    suggestion_result = generate_suggestions(
        profile,
        skills,
        education,
        projects,
        experience,
        certifications,
        achievements,
        ats_result,
        keyword_result
    )


    # --------------------------------
    # 18. Check Resume Completeness
    # --------------------------------

    completeness_result = check_completeness(
        profile,
        skills,
        education,
        projects,
        experience,
        certifications,
        achievements
    )


    # =================================
    # DATABASE STORAGE
    # =================================

    connection = get_connection()
    cursor = connection.cursor()


    # --------------------------------
    # 19. Save basic resume information
    # --------------------------------

    cursor.execute(
        """
        INSERT INTO resumes
        (
            file_name,
            file_type,
            extracted_text,
            ats_score,
            ats_health
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            file.filename,
            extension,
            text,
            ats_result["ats_score"],
            ats_result["health"]
        )
    )

    resume_id = cursor.fetchone()[0]


    # --------------------------------
    # 20. Save profile information
    # --------------------------------

    cursor.execute(
        """
        INSERT INTO resume_profiles
        (
            resume_id,
            name,
            email,
            phone,
            linkedin,
            github,
            website
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            resume_id,
            profile.get("name"),
            profile.get("email"),
            profile.get("phone"),
            profile.get("linkedin"),
            profile.get("github"),
            profile.get("website")
        )
    )


    # --------------------------------
    # 21. Save education information
    # --------------------------------

    degrees = education.get(
        "degrees",
        []
    )

    years = education.get(
        "years",
        []
    )

    for index, degree in enumerate(degrees):

        start_year = None
        end_year = None

        if len(years) >= (index + 1) * 2:

            try:

                start_year = int(
                    years[index * 2]
                )

                end_year = int(
                    years[index * 2 + 1]
                )

            except ValueError:

                start_year = None
                end_year = None

        cursor.execute(
            """
            INSERT INTO resume_education
            (
                resume_id,
                degree,
                institution,
                start_year,
                end_year,
                cgpa,
                percentage
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                resume_id,
                degree,
                None,
                start_year,
                end_year,
                education.get("cgpa"),
                education.get("percentage")
            )
        )


    # --------------------------------
    # 22. Save skills information
    # --------------------------------

    for category, skill_list in skills.items():

        if isinstance(skill_list, list):

            for skill in skill_list:

                cursor.execute(
                    """
                    INSERT INTO resume_skills
                    (
                        resume_id,
                        skill_name,
                        skill_category
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        resume_id,
                        skill,
                        category
                    )
                )


    # --------------------------------
    # 23. Save project information
    # --------------------------------

    project_list = projects.get(
        "projects_found",
        []
    )

    for project_name in project_list:

        cursor.execute(
            """
            INSERT INTO resume_projects
            (
                resume_id,
                project_name,
                description,
                technologies
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                resume_id,
                project_name,
                None,
                None
            )
        )


    # --------------------------------
    # 24. Save experience information
    # --------------------------------

    experience_list = experience.get(
        "experience_found",
        []
    )

    for item in experience_list:

        role = item.get(
            "role",
            item.get("job_title")
        )

        company = item.get(
            "company"
        )

        duration = item.get(
            "duration"
        )

        start_date = item.get(
            "start_date"
        )

        end_date = item.get(
            "end_date"
        )

        if duration and not start_date:
            start_date = duration

        description = item.get(
            "description"
        )

        if isinstance(description, list):

            description = "\n".join(
                description
            )

        cursor.execute(
            """
            INSERT INTO resume_experience
            (
                resume_id,
                job_title,
                company,
                start_date,
                end_date,
                description
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                resume_id,
                role,
                company,
                start_date,
                end_date,
                description
            )
        )


    # --------------------------------
    # 25. Save certification information
    # --------------------------------

    certification_list = certifications.get(
        "certifications_found",
        []
    )

    for certification in certification_list:

        cursor.execute(
            """
            INSERT INTO resume_certifications
            (
                resume_id,
                certification_name,
                issuing_organization,
                issue_date
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                resume_id,
                certification,
                None,
                None
            )
        )


    # --------------------------------
    # 26. Save achievement information
    # --------------------------------

    achievement_list = achievements.get(
        "achievements_found",
        []
    )

    for achievement in achievement_list:

        cursor.execute(
            """
            INSERT INTO resume_achievements
            (
                resume_id,
                achievement
            )
            VALUES (%s, %s)
            """,
            (
                resume_id,
                achievement
            )
        )


    # --------------------------------
    # 27. Save ATS analysis
    # --------------------------------

    ats_breakdown = ats_result.get(
        "breakdown",
        {}
    )

    cursor.execute(
        """
        INSERT INTO resume_ats
        (
            resume_id,
            ats_score,
            health,
            personal_information_score,
            skills_score,
            education_score,
            projects_score,
            experience_score,
            certifications_score,
            achievements_score,
            resume_content_score
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            resume_id,
            ats_result.get("ats_score"),
            ats_result.get("health"),
            ats_breakdown.get(
                "personal_information",
                0
            ),
            ats_breakdown.get(
                "skills",
                0
            ),
            ats_breakdown.get(
                "education",
                0
            ),
            ats_breakdown.get(
                "projects",
                0
            ),
            ats_breakdown.get(
                "experience",
                0
            ),
            ats_breakdown.get(
                "certifications",
                0
            ),
            ats_breakdown.get(
                "achievements",
                0
            ),
            ats_breakdown.get(
                "resume_content",
                0
            )
        )
    )


    # --------------------------------
    # 28. Save keyword information
    # --------------------------------

    keyword_list = keyword_result.get(
        "keywords_found",
        []
    )

    for item in keyword_list:

        cursor.execute(
            """
            INSERT INTO resume_keywords
            (
                resume_id,
                keyword,
                occurrence_count
            )
            VALUES (%s, %s, %s)
            """,
            (
                resume_id,
                item.get("keyword"),
                item.get("count")
            )
        )


    # --------------------------------
    # 29. Save suggestion information
    # --------------------------------

    suggestion_list = suggestion_result.get(
        "suggestions",
        []
    )

    for suggestion in suggestion_list:

        cursor.execute(
            """
            INSERT INTO resume_suggestions
            (
                resume_id,
                suggestion
            )
            VALUES (%s, %s)
            """,
            (
                resume_id,
                suggestion
            )
        )


    # --------------------------------
    # 30. Save completeness information
    # --------------------------------

    cursor.execute(
        """
        INSERT INTO resume_completeness
        (
            resume_id,
            completeness_percentage,
            total_sections,
            completed_sections,
            missing_sections,
            missing_section_names
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            resume_id,
            completeness_result.get(
                "completeness_percentage"
            ),
            completeness_result.get(
                "total_sections"
            ),
            completeness_result.get(
                "completed_sections"
            ),
            completeness_result.get(
                "missing_sections"
            ),
            ", ".join(
                completeness_result.get(
                    "missing_section_names",
                    []
                )
            )
        )
    )


    # --------------------------------
    # 31. Commit all database changes
    # --------------------------------

    connection.commit()


    # --------------------------------
    # 32. Close database connection
    # --------------------------------

    cursor.close()
    connection.close()


    # --------------------------------
    # 33. Return complete result
    # --------------------------------

    return {

        "status": "success",

        "file_name": file.filename,

        "file_type": extension,

        "message": "Resume uploaded and analyzed successfully.",

        "resume_id": resume_id,

        "profile": profile,

        "skills": skills,

        "education": education,

        "projects": projects,

        "experience": experience,

        "certifications": certifications,

        "achievements": achievements,

        "ats": ats_result,

        "keywords": keyword_result,

        "suggestions": suggestion_result,

        "completeness": completeness_result,

        "extracted_text": text
    }

@app.get("/resume/{resume_id}")
def get_resume(resume_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            file_name,
            file_type,
            extracted_text,
            ats_score,
            ats_health,
            created_at
        FROM resumes
        WHERE id = %s
        """,
        (resume_id,)
    )

    resume = cursor.fetchone()

    cursor.close()
    connection.close()

    if resume is None:
        return {
            "status": "error",
            "message": "Resume not found."
        }

    return {
        "status": "success",
        "resume": {
            "id": resume[0],
            "file_name": resume[1],
            "file_type": resume[2],
            "extracted_text": resume[3],
            "ats_score": resume[4],
            "ats_health": resume[5],
            "created_at": resume[6]
        }
    }

@app.get("/resume/{resume_id}/profile")
def get_resume_profile(resume_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            name,
            email,
            phone,
            linkedin,
            github,
            website
        FROM resume_profiles
        WHERE resume_id = %s
        """,
        (resume_id,)
    )

    profile = cursor.fetchone()

    cursor.close()
    connection.close()

    if profile is None:
        return {
            "status": "error",
            "message": "Profile not found."
        }

    return {
        "status": "success",
        "profile": {
            "name": profile[0],
            "email": profile[1],
            "phone": profile[2],
            "linkedin": profile[3],
            "github": profile[4],
            "website": profile[5]
        }
    }