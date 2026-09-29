import re


# --------------------------------
# Technical Keywords
# --------------------------------

KEYWORDS = [
    "Java",
    "Python",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "PHP",
    "SQL",

    "HTML",
    "CSS",
    "React",
    "Angular",
    "Node.js",
    "Express.js",

    "Spring",
    "Spring Boot",
    "Hibernate",

    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Oracle",

    "Git",
    "GitHub",
    "Docker",
    "Postman",
    "VS Code",

    "AWS",
    "Azure",
    "Google Cloud",

    "Data Structures",
    "Algorithms",
    "OOP",
    "REST API",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Science",

    "Agile",
    "Scrum"
]


# --------------------------------
# Count Keyword
# --------------------------------

def count_keyword(text, keyword):

    pattern = r"(?<!\w)" + re.escape(
        keyword
    ) + r"(?!\w)"

    matches = re.findall(
        pattern,
        text,
        re.IGNORECASE
    )

    return len(matches)


# --------------------------------
# Analyze Keywords
# --------------------------------

def analyze_keywords(text):

    found_keywords = []

    for keyword in KEYWORDS:

        count = count_keyword(
            text,
            keyword
        )

        if count > 0:

            found_keywords.append({
                "keyword": keyword,
                "count": count
            })

    # Sort by frequency
    found_keywords.sort(
        key=lambda item: item["count"],
        reverse=True
    )

    return {

        "keywords_found": found_keywords,

        "total_unique_keywords":
            len(found_keywords),

        "total_keyword_occurrences":
            sum(
                item["count"]
                for item in found_keywords
            )
    }