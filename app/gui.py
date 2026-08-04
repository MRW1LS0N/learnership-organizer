import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk

print("GUI LOADED")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LearnershipOrganizer(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Learnership Organizer")
        self.geometry("1100x700")

        self.evidence_folder = ""

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
            state="disabled"
        )

        self.organize_button.pack(pady=20)

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.evidence_folder = folder

            self.folder_label.configure(text=folder)