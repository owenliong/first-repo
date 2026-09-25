import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from pypdf import PdfReader, PdfWriter


class PDFToolsApp:
    def __init__(self, root):
        self.root = root

        self.root.title("PDF Editor")
        self.root.geometry("750x600")
        self.root.minsize(650, 500)

        self.pdf_files = []

        self.create_interface()

    # =========================================================
    # MAIN INTERFACE
    # =========================================================

    def create_interface(self):

        # Title
        title = tk.Label(
            self.root,
            text="PDF Editor",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            self.root,
            text="Merge multiple PDFs or split a PDF into smaller files.",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 20))

        # Main buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Merge PDFs",
            width=18,
            height=2,
            font=("Segoe UI", 11, "bold"),
            command=self.show_merge
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Split PDF",
            width=18,
            height=2,
            font=("Segoe UI", 11, "bold"),
            command=self.show_split
        ).grid(row=0, column=1, padx=10)

        # Content frame
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=30,
            pady=20
        )

        self.show_merge()

    # =========================================================
    # MERGE INTERFACE
    # =========================================================

    def show_merge(self):

        self.clear_content()

        title = tk.Label(
            self.content_frame,
            text="Merge PDFs",
            font=("Segoe UI", 15, "bold")
        )
        title.pack(pady=(0, 10))

        # List frame
        list_frame = tk.Frame(self.content_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.merge_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            font=("Segoe UI", 10)
        )

        self.merge_listbox.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar = tk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.merge_listbox.yview
        )

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.merge_listbox.config(
            yscrollcommand=scrollbar.set
        )

        # Buttons
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Add PDFs",
            width=12,
            command=self.add_pdfs
        ).grid(row=0, column=0, padx=3)

        tk.Button(
            button_frame,
            text="Remove",
            width=12,
            command=self.remove_pdf
        ).grid(row=0, column=1, padx=3)

        tk.Button(
            button_frame,
            text="Move Up",
            width=12,
            command=self.move_up
        ).grid(row=0, column=2, padx=3)

        tk.Button(
            button_frame,
            text="Move Down",
            width=12,
            command=self.move_down
        ).grid(row=0, column=3, padx=3)

        tk.Button(
            button_frame,
            text="Clear",
            width=12,
            command=self.clear_pdfs
        ).grid(row=0, column=4, padx=3)

        # Merge button
        tk.Button(
            self.content_frame,
            text="MERGE PDFs",
            width=25,
            height=2,
            font=("Segoe UI", 11, "bold"),
            command=self.merge_pdfs
        ).pack(pady=10)

        self.update_merge_list()

    # =========================================================
    # MERGE FUNCTIONS
    # =========================================================

    def add_pdfs(self):

        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[
                ("PDF files", "*.pdf")
            ]
        )

        if not files:
            return

        for file in files:

            if file not in self.pdf_files:
                self.pdf_files.append(file)

        self.update_merge_list()

    def remove_pdf(self):

        selection = self.merge_listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "No selection",
                "Please select a PDF first."
            )
            return

        index = selection[0]

        del self.pdf_files[index]

        self.update_merge_list()

    def move_up(self):

        selection = self.merge_listbox.curselection()

        if not selection:
            return

        index = selection[0]

        if index == 0:
            return

        self.pdf_files[index], self.pdf_files[index - 1] = (
            self.pdf_files[index - 1],
            self.pdf_files[index]
        )

        self.update_merge_list()

        self.merge_listbox.selection_set(index - 1)

    def move_down(self):

        selection = self.merge_listbox.curselection()

        if not selection:
            return

        index = selection[0]

        if index == len(self.pdf_files) - 1:
            return

        self.pdf_files[index], self.pdf_files[index + 1] = (
            self.pdf_files[index + 1],
            self.pdf_files[index]
        )

        self.update_merge_list()

        self.merge_listbox.selection_set(index + 1)

    def clear_pdfs(self):

        self.pdf_files = []

        self.update_merge_list()

    def update_merge_list(self):

        if not hasattr(self, "merge_listbox"):
            return

        self.merge_listbox.delete(0, tk.END)

        for i, file in enumerate(self.pdf_files, start=1):

            filename = Path(file).name

            self.merge_listbox.insert(
                tk.END,
                f"{i}. {filename}"
            )

    def merge_pdfs(self):

        if len(self.pdf_files) < 2:

            messagebox.showwarning(
                "Not enough PDFs",
                "Please select at least two PDF files."
            )

            return

        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            initialfile="merged.pdf",
            filetypes=[
                ("PDF files", "*.pdf")
            ]
        )

        if not output_file:
            return

        try:

            writer = PdfWriter()

            for pdf in self.pdf_files:

                writer.append(pdf)

            with open(output_file, "wb") as file:

                writer.write(file)

            writer.close()

            messagebox.showinfo(
                "Success",
                "PDFs successfully merged!\n\n"
                f"Saved as:\n{output_file}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not merge PDFs.\n\n{error}"
            )

    # =========================================================
    # SPLIT INTERFACE
    # =========================================================

    def show_split(self):

        self.clear_content()

        title = tk.Label(
            self.content_frame,
            text="Split PDF",
            font=("Segoe UI", 15, "bold")
        )

        title.pack(pady=(0, 15))

        # Select PDF
        file_frame = tk.Frame(self.content_frame)
        file_frame.pack(fill=tk.X, pady=5)

        self.split_file_label = tk.Label(
            file_frame,
            text="No PDF selected",
            anchor="w",
            relief=tk.SUNKEN,
            padx=5
        )

        self.split_file_label.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        tk.Button(
            file_frame,
            text="Select PDF",
            width=15,
            command=self.select_split_pdf
        ).pack(side=tk.RIGHT, padx=(10, 0))

        # Page information
        self.page_info = tk.Label(
            self.content_frame,
            text="",
            font=("Segoe UI", 10)
        )

        self.page_info.pack(pady=10)

        # Split method
        method_label = tk.Label(
            self.content_frame,
            text="Split method:",
            font=("Segoe UI", 10, "bold")
        )

        method_label.pack(anchor="w")

        self.split_method = tk.StringVar(
            value="individual"
        )

        tk.Radiobutton(
            self.content_frame,
            text="Every page separately",
            variable=self.split_method,
            value="individual",
            command=self.update_split_options
        ).pack(anchor="w")

        tk.Radiobutton(
            self.content_frame,
            text="Every N pages",
            variable=self.split_method,
            value="chunks",
            command=self.update_split_options
        ).pack(anchor="w")

        tk.Radiobutton(
            self.content_frame,
            text="Custom page ranges",
            variable=self.split_method,
            value="ranges",
            command=self.update_split_options
        ).pack(anchor="w")

        # Options
        self.options_frame = tk.Frame(
            self.content_frame
        )

        self.options_frame.pack(
            fill=tk.X,
            pady=15
        )

        # N pages
        self.chunk_label = tk.Label(
            self.options_frame,
            text="Pages per file:"
        )

        self.chunk_entry = tk.Entry(
            self.options_frame,
            width=10
        )

        self.chunk_entry.insert(0, "5")

        # Custom ranges
        self.range_label = tk.Label(
            self.options_frame,
            text="Page ranges:"
        )

        self.range_entry = tk.Entry(
            self.options_frame,
            width=35
        )

        self.range_entry.insert(
            0,
            "1-5, 8-10, 15"
        )

        # Output folder
        output_frame = tk.Frame(
            self.content_frame
        )

        output_frame.pack(
            fill=tk.X,
            pady=10
        )

        self.output_folder_label = tk.Label(
            output_frame,
            text="Output folder: Same as input",
            anchor="w"
        )

        self.output_folder_label.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        tk.Button(
            output_frame,
            text="Choose Folder",
            command=self.select_output_folder
        ).pack(side=tk.RIGHT)

        # Split button
        tk.Button(
            self.content_frame,
            text="SPLIT PDF",
            width=25,
            height=2,
            font=("Segoe UI", 11, "bold"),
            command=self.split_pdf
        ).pack(pady=15)

        self.split_file = None
        self.output_folder = None

        self.update_split_options()

    # =========================================================
    # SPLIT FUNCTIONS
    # =========================================================

    def select_split_pdf(self):

        file = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[
                ("PDF files", "*.pdf")
            ]
        )

        if not file:
            return

        self.split_file = file

        self.split_file_label.config(
            text=Path(file).name
        )

        try:

            reader = PdfReader(file)

            page_count = len(reader.pages)

            self.page_info.config(
                text=f"Number of pages: {page_count}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not open PDF.\n\n{error}"
            )

    def update_split_options(self):

        # Remove previous widgets
        for widget in self.options_frame.winfo_children():
            widget.grid_forget()

        method = self.split_method.get()

        if method == "chunks":

            self.chunk_label.grid(
                row=0,
                column=0,
                padx=5
            )

            self.chunk_entry.grid(
                row=0,
                column=1,
                padx=5
            )

        elif method == "ranges":

            self.range_label.grid(
                row=0,
                column=0,
                padx=5
            )

            self.range_entry.grid(
                row=0,
                column=1,
                padx=5
            )

    def select_output_folder(self):

        folder = filedialog.askdirectory(
            title="Select output folder"
        )

        if not folder:
            return

        self.output_folder = folder

        self.output_folder_label.config(
            text=f"Output folder: {folder}"
        )

    # =========================================================
    # PAGE RANGE PARSER
    # =========================================================

    def parse_ranges(self, text, total_pages):

        ranges = []

        parts = text.split(",")

        for part in parts:

            part = part.strip()

            if not part:
                continue

            if "-" in part:

                values = part.split("-")

                if len(values) != 2:
                    raise ValueError(
                        f"Invalid range: {part}"
                    )

                start = int(values[0])
                end = int(values[1])

            else:

                start = int(part)
                end = start

            if start < 1 or end > total_pages:
                raise ValueError(
                    f"Page range {part} is outside "
                    f"the PDF ({total_pages} pages)."
                )

            if start > end:
                raise ValueError(
                    f"Invalid range: {part}"
                )

            ranges.append(
                (start - 1, end - 1)
            )

        return ranges

    # =========================================================
    # SPLIT PDF
    # =========================================================

    def split_pdf(self):

        if not self.split_file:

            messagebox.showwarning(
                "No PDF selected",
                "Please select a PDF first."
            )

            return

        try:

            reader = PdfReader(
                self.split_file
            )

            total_pages = len(reader.pages)

            method = self.split_method.get()

            # -------------------------------------------------
            # Determine output folder
            # -------------------------------------------------

            if self.output_folder:

                output_folder = Path(
                    self.output_folder
                )

            else:

                output_folder = Path(
                    self.split_file
                ).parent

            output_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            base_name = Path(
                self.split_file
            ).stem

            # -------------------------------------------------
            # Individual pages
            # -------------------------------------------------

            if method == "individual":

                for i, page in enumerate(
                    reader.pages,
                    start=1
                ):

                    writer = PdfWriter()

                    writer.add_page(page)

                    output_file = (
                        output_folder
                        / f"{base_name}_page_{i}.pdf"
                    )

                    with open(
                        output_file,
                        "wb"
                    ) as file:

                        writer.write(file)

            # -------------------------------------------------
            # Every N pages
            # -------------------------------------------------

            elif method == "chunks":

                try:

                    pages_per_file = int(
                        self.chunk_entry.get()
                    )

                except ValueError:

                    raise ValueError(
                        "Pages per file must be a number."
                    )

                if pages_per_file <= 0:

                    raise ValueError(
                        "Pages per file must be greater than 0."
                    )

                file_number = 1

                for start in range(
                    0,
                    total_pages,
                    pages_per_file
                ):

                    end = min(
                        start + pages_per_file,
                        total_pages
                    )

                    writer = PdfWriter()

                    for i in range(
                        start,
                        end
                    ):

                        writer.add_page(
                            reader.pages[i]
                        )

                    output_file = (
                        output_folder
                        / f"{base_name}_part_{file_number}.pdf"
                    )

                    with open(
                        output_file,
                        "wb"
                    ) as file:

                        writer.write(file)

                    file_number += 1

            # -------------------------------------------------
            # Custom ranges
            # -------------------------------------------------

            elif method == "ranges":

                ranges = self.parse_ranges(
                    self.range_entry.get(),
                    total_pages
                )

                if not ranges:

                    raise ValueError(
                        "Please enter at least one page range."
                    )

                for number, (start, end) in enumerate(
                    ranges,
                    start=1
                ):

                    writer = PdfWriter()

                    for i in range(
                        start,
                        end + 1
                    ):

                        writer.add_page(
                            reader.pages[i]
                        )

                    output_file = (
                        output_folder
                        / f"{base_name}_range_{number}.pdf"
                    )

                    with open(
                        output_file,
                        "wb"
                    ) as file:

                        writer.write(file)

            messagebox.showinfo(
                "Success",
                "PDF successfully split!\n\n"
                f"Files saved to:\n{output_folder}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not split PDF.\n\n{error}"
            )

    # =========================================================
    # UTILITY
    # =========================================================

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()


# =============================================================
# START APPLICATION
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = PDFToolsApp(root)

    root.mainloop()