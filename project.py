import tkinter as tk
from tkinter import messagebox,PhotoImage,Label
import mysql.connector


history_window = None
current_user = None

# ---------------------- TOOLS & FUNCTIONS ------------------------
# Clear all widgets from a window
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

# Toggle password visibility
def toggle_password(entry_widget, var):
    entry_widget.config(show="" if var.get() else "*")

# Check password strength
def check_password_strength(password):
    length = len(password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_num = any(char.isdigit() for char in password)
    has_special = any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|" for char in password)
    score = sum([length >= 8, has_upper, has_lower, has_num, has_special])
    
    if score <= 2:
        return "Weak", "red", "Try adding numbers, symbols, and uppercase letters."
    elif score == 3 or score == 4:
        return "Medium", "orange", "You're getting there! Add more variety to strengthen it."
    else:
        return "Strong", "green", "Excellent! Your password is strong."
    

# User Guide button simulation
def user_guide():
    messagebox.showinfo("User Guide", 
        "💡 Sample Questions:\n"
        "- How to make a strong password?\n"
        "✔ Use uppercase, lowercase, numbers & symbols, min 8 characters.\n\n"
        "- What is secure password?\n"
        "✔ Avoid personal info. Use unique passwords. Enable 2FA if possible.\n\n"
        "- How to protect my account?\n"
        "✔ Don’t share passwords. Logout after use. Use strong credentials.")

# ---------------------- INTERFACE 1: WELCOME PAGE ------------------------
def welcome_page(window):
    clear_window(window)
    window.configure(bg="#F7E7CE")  

    background_image = tk.PhotoImage(file=r"C:/Users/nurul/Downloads/Untitled design.png")
    background_label = tk.Label(window, image=background_image)
    background_label.place(relwidth=1, relheight=1) 

    background_label.image = background_image


    label = tk.Label(window, text="WELCOME TO PASSWORD STRENGTH CHECKER ", 
                 font=("Lobster", 17, "bold"), fg="beige", bg="#520000")
    label.place(relx=0.5, rely=0.08, anchor="center")
   

# Sign Up button
    def on_enter(e):
        sign_up_button.config(bg="#D4B29A")  

    def on_leave(e):
        sign_up_button.config(bg="#FFF5E1")  

    sign_up_button = tk.Button(window, text="--- Sign Up ---", command=lambda: signup_page(window), 
                         font=("Calibri", 11, "normal"), bg="#FFF5E1", fg="black",
                         width=14, height=2)
    sign_up_button.place(relx=0.40, rely=0.75, anchor="center")

    sign_up_button.bind("<Enter>", on_enter)
    sign_up_button.bind("<Leave>", on_leave)

# Log In button
    def on_enter_log_in(e):
        log_in_button.config(bg="#D4B29A")  

    def on_leave_log_in(e):
        log_in_button.config(bg="#FFF5E1")  

    log_in_button = tk.Button(window, text="--- Log In ---", command=lambda: login_page(window), 
                         font=("Calibri", 11, "normal"), bg="#FFF5E1", fg="black",
                         width=14, height=2)
    log_in_button.place(relx=0.60, rely=0.75, anchor="center")

    log_in_button.bind("<Enter>", on_enter_log_in)
    log_in_button.bind("<Leave>", on_leave_log_in)

# User Guide button
    def on_enter_user_guide(e):
        user_guide_button.config(bg="#D4B29A")  
    def on_leave_user_guide(e):
        user_guide_button.config(bg="#FFF5E1") 

    user_guide_button = tk.Button(window, text="User Guide", command= user_guide, 
                                  font=("Calibri", 11, "normal"), bg="#FFF5E1", fg="black",
                                  width=12, height=2) 
    user_guide_button.place(relx=0.5, rely=0.85, anchor="center")

    user_guide_button.bind("<Enter>", on_enter_user_guide)
    user_guide_button.bind("<Leave>", on_leave_user_guide)

# ---------------------- INTERFACE 2: SIGN UP ------------------------
def signup_page(window):
    clear_window(window)
    window.configure(bg="#520000")

    tk.Label(window, text="FIRST TIME HERE? PLEASE SIGN UP", font=("Helvetica", 16, "bold"), fg="beige", bg="#520000").pack(pady=15)

    tk.Label(window, text="Username:",fg="beige", bg="#520000").pack()
    username_entry = tk.Entry(window)
    username_entry.pack()

    tk.Label(window, text="Email:",fg="beige", bg="#520000").pack()
    email_entry = tk.Entry(window)
    email_entry.pack()

    tk.Label(window, text="Password:",fg="beige", bg="#520000").pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()
    show1 = tk.BooleanVar()
    tk.Checkbutton(window, text="Show", variable=show1, command=lambda: toggle_password(password_entry, show1), fg="beige",bg="#520000").pack()

    tk.Label(window, text="Confirm Password:",fg="beige", bg="#520000").pack()
    confirm_entry = tk.Entry(window, show="*")
    confirm_entry.pack()
    show2 = tk.BooleanVar()
    tk.Checkbutton(window, text="Show", variable=show2, command=lambda: toggle_password(confirm_entry, show2),fg="beige" ,bg="#520000").pack()

    tk.Button(window, text="Sign Up", command=lambda:signup_user(username_entry,email_entry,password_entry,confirm_entry,window)).pack(pady=10)
    tk.Label(window, text="Already have an account?", fg="beige" ,bg="#520000").pack()
    tk.Button(window, text="Go to Login", command=lambda: login_page(window)).pack()
    tk.Button(window, text="Back", command=lambda: welcome_page(window)).pack(pady=10)
    tk.Button(window, text="User Guide", command=user_guide).pack()


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="password_checker"
    )
cursor = conn.cursor()

def signup_user(username_entry, email_entry, password_entry, confirm_entry, window):
    u = username_entry.get()
    e = email_entry.get()
    p = password_entry.get()
    c = confirm_entry.get()

    if not u or not e or not p or not c:
        messagebox.showerror("Error", "All fields are required.")
    elif p != c:
        messagebox.showerror("Error", "Passwords do not match.")
    else:
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (u, e, p))
            conn.commit()
            messagebox.showinfo("Success", "Account created!")
            main_checker_page(window)
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
             
# ---------------------- INTERFACE 3: LOGIN ------------------------
def login_page(window):
    clear_window(window)
    window.configure(bg="#520000")

    tk.Label(window, text="HI! LOGIN HERE", font=("Helvetica", 16, "bold"), fg= "beige",bg="#520000").pack(pady=15)

    tk.Label(window, text="Username:", fg="beige",bg="#520000").pack()
    username_entry = tk.Entry(window)
    username_entry.pack()

    tk.Label(window, text="Password:",fg="beige", bg="#520000").pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()
    show = tk.BooleanVar()
    tk.Checkbutton(window, text="Show", variable=show, command=lambda: toggle_password(password_entry, show), fg= "beige",bg="#520000").pack()

    def login_user(username_entry,password_entry,window):
        u = username_entry.get()
        p = password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (u, p))
        user = cursor.fetchone()

        if user:
            global current_user
            current_user = u
            
            messagebox.showinfo("Login Success", f"Welcome {u}!")
            main_checker_page(window)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    

    tk.Button(window, text="Login", command=lambda: login_user(username_entry,password_entry,window)).pack(pady=10)
    tk.Button(window, text="Back", command=lambda: signup_page(window)).pack()

    tk.Button(window, text="User Guide", command= user_guide).pack()

# ---------------------- INTERFACE 4: PASSWORD STRENGTH CHECKER ------------------------
def main_checker_page(window):
    clear_window(window)
    window.configure(bg="#520000")

    tk.Label(window, text="WELCOME TO PASSWORD STRENGTH CHECKER 📊✨", font=("Helvetica", 16, "bold"), bg="#520000", fg="beige").pack(pady=10)
    tk.Label(window, text="CHECK YOUR PASSWORD STRENGTH HERE 🌻🌼", font=("Helvetica", 14),fg="beige", bg="#520000").pack()

    tk.Label(window, text="Enter Password:",fg="beige" ,bg="#520000").pack(pady=(20, 5))
    check_password_entry = tk.Entry(window, show="*")
    check_password_entry.pack()
    show = tk.BooleanVar()
    tk.Checkbutton(window, text="Show Password", variable=show, command=lambda: toggle_password(check_password_entry, show),fg="beige" ,bg="#520000").pack(pady=(5, 20))

    result_label = tk.Label(window, text="", bg="#520000",fg="beige", font=("Helvetica", 12, "bold"))
    result_label.pack(pady=5)
    suggestion_label = tk.Label(window, text="", bg="#520000")
    suggestion_label.pack()

    def check():
        print("check() function was triggered")
        pw = check_password_entry.get()
        if not pw:
            result_label.config(text="Please enter a password.", fg="red")
            suggestion_label.config(text="")
        else:
            level, color, suggestion = check_password_strength(pw)
            result_label.config(text=f"Password Strength: {level}", fg=color)
            suggestion_label.config(text=suggestion, fg="beige")

    tk.Button(window, text="Check Password", command=check).pack(pady=10)

    tips = [
        "💙 Weak passwords are easy for hackers to guess and can cause accounts to be hacked.",
        "💜 A strong password will protect personal data and keep your accounts secure.",
        "💖 Use a combination of uppercase and lowercase letters, numbers and symbols.",
        "💝 Do not use personal information such as name, IC and date of birth."
    ]
    for tip in tips:
        tk.Label(window, text=tip, wraplength=500,fg="beige", bg="#520000").pack(anchor="center", padx=30)

    tk.Button(window, text="Home", command=lambda: welcome_page(window)).pack(pady=10)
    tk.Button(window, text="User Guide", command=user_guide).pack()
    tk.Button(window, text="Check & View History", command=lambda: check_and_view_history(window, current_user)).pack(pady=10)

    def check():

            pw = check_password_entry.get().strip()
            print(f"Password entered: {pw}")

            if not pw:
                result_label.config(text="Please enter a password.", fg="red")
                return
            
            level, color, suggestion = check_password_strength(pw)
            result_label.config(text=f"Password Strength: {level}", fg=color)
            suggestion_label.config(text=suggestion, fg="beige")

            try:
                cursor.execute("INSERT INTO password_history (check_password, password_strength) VALUES (%s, %s)", (pw, level))
                conn.commit()
                print(f"Saved history: {pw}, Strength: {level}")

            except mysql.connector.Error as err:
                    print(f"Error saving history: {err}")


    def view_password_history(window,username):
        print(f"Opening history window for: {username}")

        global history_window
        if history_window and history_window.winfo_exists():
            history_window.lift()

            return

        history_window = tk.Toplevel(window)

        history_window.title("Password Strength History")
        history_window.geometry("500x400")
        history_window.configure(bg="#520000")

        cursor.execute("SELECT check_password,password_strength FROM password_history ORDER BY checked_at DESC")
        history_data = cursor.fetchall()
        print(f"History Data Retrieved: {history_data}")

        tk.Label(history_window, text="Password Strength History", font=("Helvetica", 14, "bold"), fg="beige", bg="#520000").pack(pady=10)

        if not history_data:
            tk.Label(history_window, text="No history found.", fg="beige", bg="#520000").pack()
        else:
            for check_password,strength in history_data:
                tk.Label(history_window, text=f"Password: {check_password} | Strength: {strength}", fg="beige", bg="#520000").pack()

    def check_and_view_history(window, username):
        check()  
        view_password_history(window, username)  
    
# ---------------------- START THE APP ------------------------
def run_app():
    root = tk.Tk()
    root.title("Password Strength Checker")
    root.geometry("650x650")
    welcome_page(root)
    root.mainloop()

# Run it
run_app()