import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import pikepdf
import os

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger & Compressor")
        self.root.geometry("400x300")
        self.pdf_files = []

        self.label = tk.Label(root, text="PDF Merger & Compressor", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.add_button = tk.Button(root, text="Add PDFs", command=self.add_pdfs)
        self.add_button.pack(pady=5)

        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=5)

        self.compress_button = tk.Button(root, text="Compress Merged PDF", command=self.compress_pdf)
        self.compress_button.pack(pady=5)

        self.status = tk.Label(root, text="", fg="green")
        self.status.pack(pady=10)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self.pdf_files.extend(files)
        self.status.config(text=f"Added {len(files)} files.")

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("No files", "Please add PDF files to merge.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        merger = PdfMerger()

        try:
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(output_path)
            merger.close()
            self.merged_file = output_path
            self.status.config(text="PDFs merged successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def compress_pdf(self):
        if not hasattr(self, 'merged_file'):
            messagebox.showwarning("No merged file", "Merge PDFs before compressing.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        try:
            pdf = pikepdf.open(self.merged_file)
            pdf.save(output_path, optimize_version=True, compress_streams=True)
            self.status.config(text="PDF compressed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)

    root.mainloop()
