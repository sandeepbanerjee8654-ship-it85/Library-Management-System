import sqlite3
from tkinter import *
from tkinter import messagebox

# Database Setup
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 title TEXT NOT NULL,
 author TEXT NOT NULL,
 status TEXT NOT NULL
)
''')
conn.commit()

# Functions
def add_book():
    title = title_entry.get()
    author = author_entry.get()

    if title and author:
        cursor.execute(
            "INSERT INTO books (title, author, status) VALUES (?, ?, ?)",
            (title, author, "Available")
        )
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")
        clear_entries()
        view_books()
    else:
        messagebox.showwarning("Input Error", "Please enter both Title and Author.")
def view_books():
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        listbox.insert(END, f"{row[0]}. {row[1]} by {row[2]} — [{row[3]}]")

def search_book():
    query = search_entry.get()
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                   ('%' + query + '%', '%' + query + '%'))
    for row in cursor.fetchall():
        listbox.insert(END, f"{row[0]}. {row[1]} by {row[2]} — [{row[3]}]")

def issue_book():
    try:
        selected = listbox.get(listbox.curselection())
        book_id = selected.split('.')[0]
        cursor.execute("UPDATE books SET status=? WHERE id=?", ("Issued", book_id))
        conn.commit()
        messagebox.showinfo("Success", "Book issued!")
        view_books()
    except:
        messagebox.showwarning("Error", "Please select a book.")

def return_book():
    try:
        selected = listbox.get(listbox.curselection())
        book_id = selected.split('.')[0]
        cursor.execute("UPDATE books SET status=? WHERE id=?", ("Available", book_id))
        conn.commit()
        messagebox.showinfo("Success", "Book returned!")
        view_books()
    except:
        messagebox.showwarning("Error", "Please select a book.")

def delete_book():
    try:
        selected = listbox.get(listbox.curselection())
        book_id = selected.split('.')[0]
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Book removed from library.")
        view_books()
    except:
        messagebox.showwarning("Error", "Please select a book.")

def clear_entries():
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    search_entry.delete(0, END)

# GUI
root = Tk()
root.title("Library Management System")
root.geometry("600x500")
root.config(bg="#eaf4fc")

Label(root, text="■ Library Management System", font=("Arial", 18, "bold"), bg="#eaf4fc").pack(pady=10)

# Add Book Frame
frame1 = Frame(root, bg="#eaf4fc")
frame1.pack(pady=5)

Label(frame1, text="Title:", bg="#eaf4fc").grid(row=0, column=0, padx=5, pady=2)
title_entry = Entry(frame1, width=25)
title_entry.grid(row=0, column=1)

Label(frame1, text="Author:", bg="#eaf4fc").grid(row=1, column=0, padx=5, pady=2)
author_entry = Entry(frame1, width=25)
author_entry.grid(row=1, column=1)

Button(frame1, text="Add Book", command=add_book, bg="#4CAF50", fg="white").grid(row=0, column=2, rowspan=2, padx=10)

# Search Frame
frame2 = Frame(root, bg="#eaf4fc")
frame2.pack(pady=5)

Label(frame2, text="Search:", bg="#eaf4fc").grid(row=0, column=0, padx=5)
search_entry = Entry(frame2, width=25)
search_entry.grid(row=0, column=1)

Button(frame2, text="Search", command=search_book, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5)
Button(frame2, text="View All", command=view_books, bg="#9C27B0", fg="white").grid(row=0, column=3, padx=5)

# Book List Display
listbox = Listbox(root, width=70, height=15)
listbox.pack(pady=10)

# Action Buttons
frame3 = Frame(root, bg="#eaf4fc")
frame3.pack(pady=5)

Button(frame3, text="Issue", command=issue_book, bg="#FF9800", fg="white", width=10).grid(row=0, column=0, padx=5)
Button(frame3, text="Return", command=return_book, bg="#009688", fg="white", width=10).grid(row=0, column=1, padx=5)
Button(frame3, text="Delete", command=delete_book, bg="#F44336", fg="white", width=10).grid(row=0, column=2, padx=5)
Button(frame3, text="Clear", command=clear_entries, bg="#607D8B", fg="white", width=10).grid(row=0, column=3, padx=5)

view_books()
root.mainloop()
