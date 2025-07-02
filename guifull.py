import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db_config import get_connection

conn = get_connection()
cursor = conn.cursor()

class RubyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RUBY Hospital System")
        self.root.configure(bg="white")

        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(padx=30, pady=30)

        form_frame = tk.Frame(main_frame, bg="white")
        form_frame.pack(side="left", padx=(0, 50), anchor="n")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        form_inner = tk.Frame(form_frame, bg="white")
        form_inner.pack(pady=60)

        tk.Label(form_inner, text="RUBY HOSPITAL LOGIN", font=("Helvetica", 20, "bold"), bg="white").pack(pady=15)
        tk.Label(form_inner, text="Username:", font=("Helvetica", 12), bg="white").pack(anchor="w")
        tk.Entry(form_inner, textvariable=self.username, font=("Helvetica", 12), width=30).pack(pady=5)
        tk.Label(form_inner, text="Password:", font=("Helvetica", 12), bg="white").pack(anchor="w")
        tk.Entry(form_inner, textvariable=self.password, show="*", font=("Helvetica", 12), width=30).pack(pady=5)
        ttk.Button(form_inner, text="Login", command=self.login).pack(pady=10)
        ttk.Button(form_inner, text="Register", command=self.register).pack()

        image_frame = tk.Frame(main_frame, bg="white")
        image_frame.pack(side="left")

        img = Image.open("bg.png")
        resized = img.resize((img.width // 2, img.height // 2))
        self.bg_img = ImageTk.PhotoImage(resized)
        tk.Label(image_frame, image=self.bg_img, bg="white").pack()

    def login(self):
        uname = self.username.get()
        pwd = self.password.get()
        cursor.execute("SELECT password FROM user_data WHERE username=%s", (uname,))
        result = cursor.fetchone()
        if result and result[0] == pwd:
            messagebox.showinfo("Success", "Login Successful")
            self.root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        uname = self.username.get()
        pwd = self.password.get()
        try:
            cursor.execute("INSERT INTO user_data VALUES (%s, %s)", (uname, pwd))
            conn.commit()
            messagebox.showinfo("Success", "Registered Successfully")
        except:
            messagebox.showerror("Error", "Username already exists")

def open_dashboard():
    win = tk.Tk()
    win.title("RUBY Dashboard")
    win.geometry("1100x600")
    win.config(bg="#f0f9ff")

    def get_count(table):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return cursor.fetchone()[0]

    def show_table(table, columns):
        for widget in data_frame.winfo_children():
            widget.destroy()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        tree = ttk.Treeview(data_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        for row in rows:
            tree.insert("", tk.END, values=row)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        def edit_selected():
            selected = tree.focus()
            if not selected:
                messagebox.showerror("Error", "Please select a row to edit.")
                return
            current_values = tree.item(selected)["values"]
            open_edit_popup(table, columns, current_values)

        ttk.Button(data_frame, text="Edit Selected", command=edit_selected).pack(pady=5)

    def open_add_popup(title, fields, insert_query):
        popup = tk.Toplevel(win)
        popup.title(title)
        popup.geometry("400x400")
        popup.config(bg="white")

        entries = {}
        for field in fields:
            tk.Label(popup, text=field, bg="white", anchor="w").pack(pady=5)
            var = tk.StringVar()
            entry = tk.Entry(popup, textvariable=var, width=30)
            entry.pack()
            entries[field] = var

        def submit_data():
            values = [v.get().strip() for v in entries.values()]
            if any(v == "" for v in values):
                messagebox.showerror("Error", "Please fill all fields.")
                return
            try:
                cursor.execute(insert_query, values)
                conn.commit()
                messagebox.showinfo("Success", f"{title} added successfully!")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to insert data:\n{str(e)}")

        ttk.Button(popup, text="Submit", command=submit_data).pack(pady=15)

    def open_edit_popup(table, columns, current_values):
        popup = tk.Toplevel(win)
        popup.title("Edit Entry")
        popup.geometry("400x400")
        popup.config(bg="white")

        entries = {}
        for idx, col in enumerate(columns):
            tk.Label(popup, text=col, bg="white").pack(pady=5)
            var = tk.StringVar(value=str(current_values[idx]))
            entry = tk.Entry(popup, textvariable=var, width=30)
            entry.pack()
            entries[col] = var

        def submit_update():
            updated_values = [v.get().strip() for v in entries.values()]
            if any(v == "" for v in updated_values):
                messagebox.showerror("Error", "All fields must be filled.")
                return
            try:
                set_clause = ", ".join(f"`{col}`=%s" for col in columns)
                where_clause = " AND ".join(f"`{col}`=%s" for col in columns)
                full_query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
                params = updated_values + list(current_values)
                cursor.execute(full_query, params)
                conn.commit()
                messagebox.showinfo("Success", "Record updated successfully!")
                popup.destroy()
                show_table(table, columns)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update:\n{str(e)}")

        ttk.Button(popup, text="Submit", command=submit_update).pack(pady=20)

    stats = [
        f"👥 Patients: {get_count('patient_detail')}",
        f"🩺 Doctors: {get_count('doctor_details')}",
        f"👩‍⚕️ Nurses: {get_count('nurse_details')}",
        f"🧹 Staff: {get_count('other_workers_details')}"
    ]

    stats_frame = tk.Frame(win, bg="#f0f9ff")
    stats_frame.pack()
    for i, stat in enumerate(stats):
        tk.Label(stats_frame, text=stat, font=("Segoe UI", 11, "bold"), bg="#f0f9ff").grid(row=0, column=i, padx=15)

    btn_frame = tk.Frame(win, bg="#f0f9ff")
    btn_frame.pack(pady=10)

    # View Buttons
    ttk.Button(btn_frame, text="View Patients", width=20,
               command=lambda: show_table("patient_detail", ["Name", "Sex", "Age", "Address", "Contact"])).grid(row=0, column=0, padx=10)

    ttk.Button(btn_frame, text="View Doctors", width=20,
               command=lambda: show_table("doctor_details", ["Name", "Specialisation", "Age", "Address", "Contact", "Visiting Fees", "Monthly Salary"])).grid(row=0, column=1, padx=10)

    ttk.Button(btn_frame, text="View Nurses", width=20,
               command=lambda: show_table("nurse_details", ["Name", "Age", "Address", "Contact", "Monthly Salary"])).grid(row=0, column=2, padx=10)

    ttk.Button(btn_frame, text="View Other Staff", width=20,
               command=lambda: show_table("other_workers_details", ["Name", "Age", "Address", "Contact", "Monthly Salary"])).grid(row=0, column=3, padx=10)

    # Add Buttons
    ttk.Button(btn_frame, text="+ Add Patient", width=20,
               command=lambda: open_add_popup("Add Patient",
                                              ["Name", "Sex", "Age", "Address", "Contact"],
                                              "INSERT INTO patient_detail (Name, Sex, Age, Address, Contact) VALUES (%s, %s, %s, %s, %s)")).grid(row=1, column=0, pady=5)

    ttk.Button(btn_frame, text="+ Add Doctor", width=20,
               command=lambda: open_add_popup("Add Doctor",
                                              ["Name", "Specialisation", "Age", "Address", "Contact", "Visiting Fees", "Monthly Salary"],
                                              "INSERT INTO doctor_details (Name, Specialisation, Age, Address, Contact, `Visiting Fees`, `Monthly Salary`) VALUES (%s, %s, %s, %s, %s, %s, %s)")).grid(row=1, column=1, pady=5)

    ttk.Button(btn_frame, text="+ Add Nurse", width=20,
               command=lambda: open_add_popup("Add Nurse",
                                              ["Name", "Age", "Address", "Contact", "Monthly Salary"],
                                              "INSERT INTO nurse_details (Name, Age, Address, Contact, `Monthly Salary`) VALUES (%s, %s, %s, %s, %s)")).grid(row=1, column=2, pady=5)

    ttk.Button(btn_frame, text="+ Add Other Staff", width=20,
               command=lambda: open_add_popup("Add Other Staff",
                                              ["Name", "Age", "Address", "Contact", "Monthly Salary"],
                                              "INSERT INTO other_workers_details (Name, Age, Address, Contact, `Monthly Salary`) VALUES (%s, %s, %s, %s, %s)")).grid(row=1, column=3, pady=5)

    data_frame = tk.Frame(win)
    data_frame.pack(fill='both', expand=True)

    win.mainloop()

# 🎬 Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = RubyApp(root)
    root.mainloop()
