import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from pypdf import PdfWriter


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        self.pdf_files = []

        # Title
        title = tk.Label(
            root,
            text="PDF Merger",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=(15, 5))

        subtitle = tk.Label(
            root,
            text="Select and arrange PDF files, then merge them into one PDF.",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 15))

        # Main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Listbox
        self.listbox = tk.Listbox(
            main_frame,
            selectmode=tk.SINGLE,
            font=("Segoe UI", 11)
        )
        self.listbox.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # Scrollbar
        scrollbar = tk.Scrollbar(
            main_frame,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Add PDFs",
            width=14,
            command=self.add_pdfs
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Remove",
            width=14,
            command=self.remove_pdf
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Move Up",
            width=14,
            command=self.move_up
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Move Down",
            width=14,
            command=self.move_down
        ).grid(row=0, column=3, padx=5)

        # Merge button
        merge_button = tk.Button(
            root,
            text="MERGE PDFs",
            font=("Segoe UI", 12, "bold"),
            width=25,
            height=2,
            command=self.merge_pdfs
        )
        merge_button.pack(pady=(5, 20))

        # Status
        self.status = tk.Label(
            root,
            text="No PDF files selected.",
            font=("Segoe UI", 9)
        )
        self.status.pack(pady=(0, 10))

    def add_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )

        if not files:
            return

        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)

        self.update_list()

    def remove_pdf(self):
        selection = self.listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "No selection",
                "Please select a PDF to remove."
            )
            return

        index = selection[0]
        del self.pdf_files[index]

        self.update_list()

    def move_up(self):
        selection = self.listbox.curselection()

        if not selection:
            return

        index = selection[0]

        if index == 0:
            return

        self.pdf_files[index], self.pdf_files[index - 1] = (
            self.pdf_files[index - 1],
            self.pdf_files[index]
        )

        self.update_list()
        self.listbox.selection_set(index - 1)

    def move_down(self):
        selection = self.listbox.curselection()

        if not selection:
            return

        index = selection[0]

        if index == len(self.pdf_files) - 1:
            return

        self.pdf_files[index], self.pdf_files[index + 1] = (
            self.pdf_files[index + 1],
            self.pdf_files[index]
        )

        self.update_list()
        self.listbox.selection_set(index + 1)

    def update_list(self):
        self.listbox.delete(0, tk.END)

        for i, file in enumerate(self.pdf_files, start=1):
            filename = Path(file).name
            self.listbox.insert(
                tk.END,
                f"{i}. {filename}"
            )

        count = len(self.pdf_files)

        if count == 0:
            self.status.config(text="No PDF files selected.")
        elif count == 1:
            self.status.config(text="1 PDF selected.")
        else:
            self.status.config(
                text=f"{count} PDFs selected."
            )

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning(
                "No PDFs",
                "Please add at least one PDF."
            )
            return

        if len(self.pdf_files) == 1:
            messagebox.showwarning(
                "Only one PDF",
                "Please add at least two PDFs to merge."
            )
            return

        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf")
            ],
            initialfile="merged.pdf"
        )

        if not output_file:
            return

        try:
            writer = PdfWriter()

            for pdf in self.pdf_files:
                writer.append(pdf)

            with open(output_file, "wb") as output:
                writer.write(output)

            writer.close()

            messagebox.showinfo(
                "Success",
                f"PDFs successfully merged!\n\n"
                f"Saved to:\n{output_file}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not merge PDFs.\n\n{e}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()