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
    activity: str          # Informal / ISAT / PS01
    marked: bool           # True or False (PSA present?)
    attempt: int | None    # None or integer
    extension: str