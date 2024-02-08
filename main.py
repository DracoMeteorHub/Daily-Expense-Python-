import sqlite3
from tkinter import *
from tkinter import ttk
from datetime import datetime

# Function to add entry to the database
def add_entry():
    selected_option = clicked_option.get()
    amount = entry_amount.get()
    reason = entry_reason.get()
    approx_time = clicked_time.get()
    date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute("INSERT INTO entries (option, amount, reason, approx_time, date) VALUES (?, ?, ?, ?, ?)",
                   (selected_option, amount, reason, approx_time, date))
    conn.commit()

# Function to display entries in tabular format
def display_entries():
    clear_display()
    cursor.execute("SELECT option, amount, reason, approx_time, date FROM entries")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)



# Function to clear the display
def clear_display():
    for item in tree.get_children():
        tree.delete(item)

# Function to clear the database
def clear_database():
    cursor.execute("DELETE FROM entries")
    conn.commit()
    clear_display()
    # refresh_entries()

# Create Tkinter window
root = Tk()
root.title("Welcome to the Chamber")

# Options
options = [
    "Friend Food",
    "Travel Expense",
    "Study Expense",
    "Order",
    "Extra Expense"
]

# Initialize option selection variable
clicked_option = StringVar(root)
clicked_option.set(options[0])  # Set the default option

# Option menu
option_menu = OptionMenu(root, clicked_option, *options)
option_menu.pack()

# Entry fields
Label(root, text="Amount:").pack()
entry_amount = Entry(root)
entry_amount.pack()

Label(root, text="Reason:").pack()
entry_reason = Entry(root)
entry_reason.pack()

Label(root, text="Approximate Time:").pack()
clicked_time = StringVar(root)
time_options = ["{}:00 - {}:00".format(i, i+4) for i in range(0, 21, 4)]
clicked_time.set(time_options[0])  # Set the default time
time_menu = OptionMenu(root, clicked_time, *time_options)
time_menu.pack()

# Button to add entry
add_button = Button(root, text="Add Entry", command=add_entry)
add_button.pack(pady=10)

# Button to display entries
display_button = Button(root, text="Display Entries", command=display_entries)
display_button.pack(pady=5)

# Button to clear display
# clear_button = Button(root, text="Clear Display", command=clear_display)
# clear_button.pack(pady=5)

# Button to clear database
clear_button = Button(root, text="Clear Database", command=clear_database)
clear_button.pack(pady=5)

# Create a Treeview widget for displaying entries
tree = ttk.Treeview(root, columns=("Option", "Amount", "Reason", "Approximate Time", "Date"), show="headings")
tree.heading("Option", text="Option")
tree.heading("Amount", text="Amount")
tree.heading("Reason", text="Reason")
tree.heading("Approximate Time", text="Approximate Time")
tree.heading("Date", text="Date")
tree.pack()

# Center-align the entries in the Treeview
for column in ("Option", "Amount", "Reason", "Approximate Time", "Date"):
    tree.column(column, anchor="center")

# Create SQLite database
conn = sqlite3.connect('entries.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY,
                    option TEXT,
                    amount INTEGER,
                    reason TEXT,
                    approx_time TEXT,
                    date TEXT)''')
conn.commit()

# Run the Tkinter event loop
root.mainloop()

# Close the database connection when the program exits
conn.close()
