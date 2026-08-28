from pathlib import Path
import re

from app.models import DocumentInfo


def parse_filename(file: Path) -> DocumentInfo | None:
    """
    Parse a learnership filename.

    Supports:

    KM
    ---
    KM01 Informal
    KM01 Formal
    KM01 ISAT
    KM01 Informal ATT 2

    PM
    ---
    PM01 PS01
    PM01 PS01 PSA
    PM06

    Extra words before/after are ignored.
    """

    stem = (
        file.stem
        .replace("_", " ")
        .replace("-", " ")
    )

    extension = file.suffix.lower()

    tokens = stem.split()

    # -----------------------------
    # Find assessment token
    # -----------------------------

    assessment_match = None

    for token in tokens:

        token = token.upper()

        if re.fullmatch(r"(KM|PM)\d{2}", token):
            assessment_match = token
            break

    if assessment_match is None:
        return None

    assessment_type = assessment_match[:2]
    assessment_number = int(assessment_match[2:])

    # Validate assessment number

    if assessment_number < 1 or assessment_number > 12:
        return None

    # -----------------------------
    # Student name
    # -----------------------------

    student = ""

    if assessment_match in tokens:

        index = tokens.index(assessment_match)

    else:

        index = tokens.index(assessment_match.title())

    if index > 0:
        student = " ".join(tokens[:index])

    # -----------------------------
    # Defaults
    # -----------------------------

    activity = None
    marked = False
    attempt = None

    upper_tokens = [t.upper() for t in tokens]

    # -----------------------------
    # KM Activities
    # -----------------------------

    if assessment_type == "KM":

        if "INFORMAL" in upper_tokens:

            activity = "Informal"

        elif "ISAT" in upper_tokens:

            activity = "ISAT"

        elif "FORMAL" in upper_tokens:

            activity = "ISAT"

        else:

            return None

    # -----------------------------
    # PM Activities
    # -----------------------------

    else:

        for token in upper_tokens:

            if re.fullmatch(r"PS\d{2}", token):

                activity = token
                break

        # PM06 etc.
        # No PS folder

        if activity is None:

            activity = None

    # -----------------------------
    # PSA
    # -----------------------------

    if "PSA" in upper_tokens:

        marked = True

    # -----------------------------
    # ATT
    # -----------------------------

    for i in range(len(upper_tokens) - 1):

        if upper_tokens[i] == "ATT":

            try:

                attempt = int(tokens[i + 1])

            except ValueError:

                pass

    return DocumentInfo(
        path=file,
        filename=file.name,
        student=student,
        assessment_type=assessment_type,
        assessment_number=assessment_number,
        activity=activity,
        marked=marked,
        attempt=attempt,
        extension=extension
    )