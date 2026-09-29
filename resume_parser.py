import fitz
from docx import Document


def extract_pdf_text(file_path):
    """Extract text from PDF resume."""

    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text() + "\n"

    document.close()

    return text


def extract_docx_text(file_path):
    """Extract text from DOCX resume."""

    document = Document(file_path)

    text = ""

    # Extract normal paragraphs
    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text += paragraph.text + "\n"

    # Extract text from tables
    for table in document.tables:

        for row in table.rows:

            for cell in row.cells:

                if cell.text.strip():
                    text += cell.text + "\n"

    return text


def clean_text(text):
    """Remove unnecessary spaces and blank lines."""

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_text(file_path, extension):
    """Select parser according to file type."""

    extension = extension.lower()

    if extension == ".pdf":

        text = extract_pdf_text(file_path)

    elif extension == ".docx":

        text = extract_docx_text(file_path)

    else:

        raise ValueError(
            "Only PDF and DOCX files are supported."
        )

    return clean_text(text)