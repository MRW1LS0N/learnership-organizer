from pathlib import Path
from app.parser import parse_filename

from app.gui import LearnershipOrganizer

if __name__ == "__main__":
    test_file = Path("Jayden Wilson KM01 Informal.pdf")

    result = parse_filename(test_file)

    print("Filename:", result.filename)
    print("Student:", result.student)
    print("Assessment:", result.assessment_type)
    print("Assessment Number:", result.assessment_number)
    print("Submission:", result.submission_type)
    print("Extension:", result.extension)
    app = LearnershipOrganizer()
    app.mainloop()