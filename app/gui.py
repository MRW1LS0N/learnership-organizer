from app.organizer import organize_document
from importlib.resources import files

from app.parser import parse_filename

import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk

from app.discovery import discover_files

print("GUI LOADED")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LearnershipOrganizer(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Learnership Organizer")
        self.geometry("1100x700")

        self.evidence_folder = ""
        self.documents = []
        self.row_lookup = {}

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Learnership Organizer",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=20)

        browse_frame = ctk.CTkFrame(self)

        browse_frame.pack(fill="x", padx=20)

        self.folder_label = ctk.CTkLabel(
            browse_frame,
            text="No Evidence folder selected",
            anchor="w"
        )

        self.folder_label.pack(side="left", padx=10, pady=10, expand=True)

        browse_button = ctk.CTkButton(
            browse_frame,
            text="Browse",
            command=self.select_folder
        )

        browse_button.pack(side="right", padx=10)

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("File", "Destination", "Status")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("File", text="File")

        self.tree.heading("Destination", text="Destination")

        self.tree.heading("Status", text="Status")

        self.tree.column("File", width=400)

        self.tree.column("Destination", width=450)

        self.tree.column("Status", width=100)

        self.tree.pack(fill="both", expand=True)

        self.organize_button = ctk.CTkButton(
            self,
            text="Organize Files",
            command=self.organize_files,
            state="disabled"
        )

        self.organize_button.pack(pady=20)

    def select_folder(self):

        folder = filedialog.askdirectory()

        if not folder:
            return

        self.evidence_folder = folder
        self.folder_label.configure(text=folder)


        files = discover_files(folder)

        for file in files:

            document = parse_filename(file)
            if document is not None:
                self.documents.append(document)

            if document is None:

                destination = "Unknown"

                status = "Invalid"

            else:

                destination = (
                    f"{document.assessment_type}/"
                    f"{document.assessment_type}{document.assessment_number:02d}"
                )

                if document.activity is not None:
                    destination += f"/{document.activity}"
                status = "Ready"

                row_id = self.tree.insert(
                    "",
                    "end",
                    values=(
                        file.name,
                        destination,
                        status
                    )
                )

            if document is not None:
                self.row_lookup[document.path] = row_id
        

        if files:
            self.organize_button.configure(state="normal")
        else:
            self.organize_button.configure(state="disabled")
    def organize_files(self):
        """
        Organize all valid parsed documents and update their table rows.
        """

        moved = 0
        skipped = 0

        for document in self.documents:
            success, message = organize_document(
                document,
                self.evidence_folder
            )

            row_id = self.row_lookup.get(document.path)

            destination = (
                f"{document.assessment_type}/"
                f"{document.assessment_type}"
                f"{document.assessment_number:02d}"
            )

            if document.activity is not None:
                destination += f"/{document.activity}"

            if success:
                moved += 1
                status = "Moved"
            else:
                skipped += 1
                status = message

            # Only update the table when the matching row exists.
            if row_id is not None:
                self.tree.item(
                    row_id,
                    values=(
                        document.filename,
                        destination,
                        status
                    )
                )

        print(f"Moved: {moved}")
        print(f"Skipped: {skipped}")