import re
from pathlib import Path

from app.models import DocumentInfo


FILENAME_PATTERN = re.compile(
    r"^(.*?)\s+"
    r"(KM|PM)"
    r"(\d{2})\s+"
    r"(Informal|ISAT|PSA|PS\d+)$",
    re.IGNORECASE,
)


def parse_filename(file_path: Path):
    """
    Parse a learnership filename.

    Example:
        Jayden Wilson KM01 Informal.pdf

    Returns:
        DocumentInfo | None
    """

    filename = file_path.stem

    match = FILENAME_PATTERN.match(filename)

    if match is None:
        return None

    student, assessment, number, submission = match.groups()

    return DocumentInfo(
        path=file_path,
        filename=file_path.name,
        student=student.strip(),
        assessment_type=assessment.upper(),
        assessment_number=int(number),
        submission_type=submission.upper(),
        extension=file_path.suffix.lower(),
    )