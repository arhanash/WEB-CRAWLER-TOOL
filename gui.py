import tkinter as tk
from tkinter import filedialog, messagebox
from crawler import crawl_and_extract_parameters  # Import the function

def start_crawl():
    url = url_entry.get()
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    db_file = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database files", "*.db")])

    if url and output_file and db_file:
        crawl_and_extract_parameters(url, output_file, db_file)
        messagebox.showinfo("Success", f"Results saved to:\nFile: {output_file}\nDatabase: {db_file}")
    else:
        messagebox.showwarning("Warning", "Please provide a URL and output paths.")

app = tk.Tk()
app.title("URL Parameter Crawler")

tk.Label(app, text="Enter URL to Crawl:").pack(pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

tk.Button(app, text="Start Crawl", command=start_crawl).pack(pady=20)

app.mainloop()

