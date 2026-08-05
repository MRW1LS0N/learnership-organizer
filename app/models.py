from dataclasses import dataclass
from pathlib import Path


@dataclass
class DocumentInfo:
    """
    Represents a learnership document after parsing.
    """

    path: Path
    filename: str

    student: str

    assessment_type: str

    assessment_number: int

    submission_type: str

    extension: str