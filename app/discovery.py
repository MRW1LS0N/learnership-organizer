from pathlib import Path

# Supported document types
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx"
}
def discover_files(evidence_folder):
    """
    Scan the Supplemented Work folder and return all supported files.

    Args:
        evidence_folder (str): Path to the Evidence folder.

    Returns:
        list[Path]: Supported documents found.
    """

    supplemented_folder = Path(evidence_folder) / "Supplemented Work"

    if not supplemented_folder.exists():
        return []

    discovered_files = [] 

    for file in supplemented_folder.iterdir():

        if (
            file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        ):
            discovered_files.append(file)

    return discovered_files
