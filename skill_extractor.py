import re


# --------------------------------
# Programming Languages
# --------------------------------

PROGRAMMING_LANGUAGES = [
    "Java",
    "Python",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "PHP",
    "SQL",
    "Dart",
    "Kotlin",
    "Swift",
    "Go",
    "Ruby"
]


# --------------------------------
# Web Technologies
# --------------------------------

WEB_TECHNOLOGIES = [
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Angular",
    "Node.js",
    "Express.js",
    "Bootstrap",
    "Tailwind CSS"
]


# --------------------------------
# Frameworks
# --------------------------------

FRAMEWORKS = [
    "Spring",
    "Spring Boot",
    "Hibernate",
    "Django",
    "Flask",
    "FastAPI",
    "React",
    "Angular",
    "Node.js",
    "Express.js"
]


# --------------------------------
# Databases
# --------------------------------

DATABASES = [
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Oracle",
    "SQLite",
    "SQL Server",
    "Firebase"
]


# --------------------------------
# Tools
# --------------------------------

TOOLS = [
    "Git",
    "GitHub",
    "GitLab",
    "Docker",
    "Postman",
    "VS Code",
    "Jupyter",
    "Jupyter Notebook",
    "Eclipse",
    "IntelliJ IDEA"
]


# --------------------------------
# Cloud Technologies
# --------------------------------

CLOUD = [
    "AWS",
    "Microsoft Azure",
    "Azure",
    "Google Cloud",
    "GCP"
]


# --------------------------------
# Other Technical Skills
# --------------------------------

OTHER_SKILLS = [
    "REST API",
    "RESTful API",
    "API",
    "Data Structures",
    "Algorithms",
    "OOP",
    "Object Oriented Programming",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Science",
    "GitHub Actions",
    "Agile",
    "Scrum"
]


def find_skills(text, skill_list):
    """
    Find skills from a predefined skill list.
    """

    found_skills = []

    for skill in skill_list:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found_skills.append(skill)

    return found_skills


def extract_skills(text):
    """
    Extract technical skills from resume text.
    """

    skills = {

        "programming_languages":
            find_skills(
                text,
                PROGRAMMING_LANGUAGES
            ),

        "web_technologies":
            find_skills(
                text,
                WEB_TECHNOLOGIES
            ),

        "frameworks":
            find_skills(
                text,
                FRAMEWORKS
            ),

        "databases":
            find_skills(
                text,
                DATABASES
            ),

        "tools":
            find_skills(
                text,
                TOOLS
            ),

        "cloud":
            find_skills(
                text,
                CLOUD
            ),

        "other_technical_skills":
            find_skills(
                text,
                OTHER_SKILLS
            )
    }

    return skills