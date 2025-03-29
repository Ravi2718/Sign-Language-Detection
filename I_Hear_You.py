import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import sys
import os
import threading

# Add the path to dataset.py to the Python path
sys.path.append(r"E:\SNS IT\final project\NSLD")

# Import back-end functions from dataset.py
from dataset import setup_database, validate_login, create_user, save_to_dataset

# Eye icon paths
eye_open_path = r"E:\SNS IT\final project\NSLD\image\eye open.png"
eye_close_path = r"E:\SNS IT\final project\NSLD\image\close-eye.png"

# Function to display the logo animation
def show_logo(root):
    image_path = r"E:\SNS IT\final project\NSLD\logo.png"
    img = Image.open(image_path)
    
    logo_label = tk.Label(root, bg="white")
    logo_label.place(relx=0.5, rely=0.5, anchor="center")  
    
    for scale in range(50, 101):  
        resized_img = img.resize((int(img.width * scale / 100), int(img.height * scale / 100)))
        tk_img = ImageTk.PhotoImage(resized_img)
        logo_label.config(image=tk_img)
        logo_label.image = tk_img
        root.update()
        time.sleep(0.03)
    
    logo_label.destroy()
    show_login_page(root)

# Function to display the login page
def show_login_page(root):
    img = Image.open(r"E:\SNS IT\final project\NSLD\login.png")
    img = ImageTk.PhotoImage(img)
    tk.Label(root, image=img, bg='white').place(x=50, y=50)

    frame = tk.Frame(root, width=500, height=500, bg="white")
    frame.place(relx=0.75, rely=0.5, anchor="center")

    def show_sign_in():
        # Clear the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Add the "Sign in" form
        heading = tk.Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 30, 'bold'))
        heading.place(x=130, y=10)

        user = create_placeholder_entry(frame, "Username", 50, 100)
        password = create_placeholder_entry(frame, "Password", 50, 180, show="*")

        # Error labels for empty fields or incorrect password
        user_error_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        user_error_label.place(x=50, y=140)  # Positioned just below the username entry field
        password_error_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        password_error_label.place(x=50, y=220)  # Positioned just below the password entry field

        # Add eye icon to toggle password visibility
        add_eye_icon(frame, password, 410, 180)

        # Bind the Enter key to trigger the login action
        frame.bind("<Return>", lambda event: on_login())

        # Label to display login messages
        login_message_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        login_message_label.place(x=40, y=220)  # Positioned below the password underline

        def on_login():
            # Clear previous error messages
            user_error_label.config(text="")
            password_error_label.config(text="")
            login_message_label.config(text="")

            # Validate if the username and password fields are not empty
            if user.get() == "" or user.get() == "Username":
                user_error_label.config(text="Please enter a username.")
                return
            if password.get() == "" or password.get() == "Password":
                password_error_label.config(text="Please enter a password.")
                return

            # Check the credentials against the SQL database (using back-end function)
            if validate_login(user.get(), password.get()):
                # Save user details to dataset.txt (using back-end function)
                save_to_dataset(user.get(), password.get())

                # Directly execute the functionality from index2.py
                execute_index2(root)

            else:
                login_message_label.config(text="Incorrect username or password.", fg="red")

        login_button = tk.Button(frame, text="Login", fg="white", bg="#57a1f8", font=('Microsoft YaHei UI Light', 10), command=on_login, width=20, height=2)
        login_button.place(x=165, y=280)

        create_user_button = tk.Button(frame, text="Create User", fg="white", bg="#57a1f8", font=('Microsoft YaHei UI Light', 10), command=show_create_user, width=20, height=2)
        create_user_button.place(x=165, y=340)

    def create_placeholder_entry(frame, placeholder, x, y, show=None):
        entry = tk.Entry(frame, width=30, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 14), show=show)
        entry.place(x=x, y=y)
        entry.insert(0, placeholder)

        # Add the underline
        tk.Frame(frame, width=400, height=3, bg='black').place(x=x, y=y+30)

        # Add a focus-out and focus-in event to handle placeholder text
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)  # Clear the placeholder text when clicked
                entry.config(fg="black")  # Change text color to black

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)  # Set back the placeholder text if the field is empty
                entry.config(fg="gray")  # Set text color back to gray (optional)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        entry.config(fg="gray")  # Set initial text color to gray for placeholder text
        return entry

    def show_create_user():
        # Clear the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Add the "Create User" form
        heading = tk.Label(frame, text='Create User', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 30, 'bold'))
        heading.place(x=100, y=10)

        user = create_placeholder_entry(frame, "Username", 50, 100)
        password = create_placeholder_entry(frame, "Password", 50, 180, show="*")
        confirm_password = create_placeholder_entry(frame, "Confirm Password", 50, 260, show="*")

        # Error labels for empty fields or password mismatch
        password_error_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        password_error_label.place(x=50, y=300)  # Positioned just below the password entry field
        confirm_password_error_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        confirm_password_error_label.place(x=60, y=300)  # Positioned just below the confirm password entry field

        # Add eye icons to toggle password visibility
        add_eye_icon(frame, password, 410, 180)
        add_eye_icon(frame, confirm_password, 410, 260)

        # Label to display create user messages
        create_user_message_label = tk.Label(frame, text="", fg="green", bg="white", font=('Microsoft YaHei UI Light', 12))
        create_user_message_label.place(x=50, y=300)  # Positioned below the confirm password entry field

        def on_submit():
            # Clear previous error messages
            password_error_label.config(text="")
            confirm_password_error_label.config(text="")
            create_user_message_label.config(text="")

            # Validate if the fields are not empty
            if user.get() == "" or user.get() == "Username":
                password_error_label.config(text="Please enter a username.")
                return
            if password.get() == "" or password.get() == "Password":
                password_error_label.config(text="Please enter a password.")
                return
            if confirm_password.get() == "" or confirm_password.get() == "Confirm Password":
                confirm_password_error_label.config(text="Please confirm your password.")
                return

            # Check if passwords match
            if password.get() != confirm_password.get():
                confirm_password_error_label.config(text="Passwords do not match!")
                return

            # Save user details to SQL database (using back-end function)
            if create_user(user.get(), password.get()):
                show_sign_in()  # Go back to the login page
            else:
                create_user_message_label.config(text="Username already exists.", fg="red")

        # Submit button
        submit_button = tk.Button(frame, text="Submit", fg="white", bg="#57a1f8", font=('Microsoft YaHei UI Light', 10), command=on_submit, width=20, height=2)
        submit_button.place(x=165, y=330)

        # Back to Login button functionality
        back_button = tk.Button(frame, text="Back to Login", fg="white", bg="#57a1f8", font=('Microsoft YaHei UI Light', 10), command=show_sign_in, width=20, height=2)
        back_button.place(x=165, y=390)  # Positioned below the submit button

        # Bind the Enter key to trigger the submit action
        frame.bind("<Return>", lambda event: on_submit())

    # Show the "Sign in" form by default
    show_sign_in()

    root.mainloop()

# Function to add eye icon for password visibility toggle
def add_eye_icon(frame, entry, x, y):
    eye_open = Image.open(eye_open_path)
    eye_open = eye_open.resize((20, 20))  # Resize the eye icon
    eye_open = ImageTk.PhotoImage(eye_open)

    eye_close = Image.open(eye_close_path)
    eye_close = eye_close.resize((20, 20))  # Resize the eye icon
    eye_close = ImageTk.PhotoImage(eye_close)

    show_password = False

    def toggle_password():
        nonlocal show_password
        if show_password:
            entry.config(show="*")
            eye_icon.config(image=eye_close)
            show_password = False
        else:
            entry.config(show="")
            eye_icon.config(image=eye_open)
            show_password = True

    eye_icon = tk.Button(frame, image=eye_close, bg="white", bd=0, command=toggle_password)
    eye_icon.place(x=x, y=y)

# Function to execute index2 functionality directly
def execute_index2(root):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Define the base directory
    BASE_DIR = r"E:\SNS IT\final project\NSLD"

    # Directly run the SignLanguageApp from index2.py
    from index2 import SignLanguageApp
    app = SignLanguageApp(root, BASE_DIR)

# Create the main window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg="#fff")
root.resizable(False, False)

# Set up the SQLite database
setup_database()

# Show the logo and then login page
show_logo(root)