from pathlib import Path
import shutil

from app.models import DocumentInfo


def organize_document(document: DocumentInfo, evidence_folder: str):
    """
    Move a parsed document into its correct folder.

    Returns:
        tuple[bool, str]
        (success, destination_path)
    """

# Decide base folder

    if document.extension == ".pdf":
        base_folder = Path(evidence_folder)

    else:
        base_folder = (
            Path(evidence_folder)
            / "Supplemented Work"
        )

    destination = (
        base_folder
        / document.assessment_type
        / f"{document.assessment_type}{document.assessment_number:02d}"
    )

    # Only create an activity folder if one exists

    if document.activity is not None:
        destination /= document.activity

    destination.mkdir(
        parents=True,
        exist_ok=True
    )

    new_file = destination / document.filename

    if new_file.exists():
        return False, "File already exists"

    shutil.move(document.path, new_file)

    return True, str(new_file)