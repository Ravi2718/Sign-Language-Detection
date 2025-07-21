import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import threading
import os

from dataset import setup_database, validate_login, create_user, save_to_dataset

# Eye icon paths
eye_open_path = os.path.join("image", "eye open.png")
eye_close_path = os.path.join("image", "close-eye.png")

# Function to display the logo animation
def show_logo(root):
    image_path = os.path.join("logo.png")
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
    img = Image.open(os.path.join("login.png"))
    img = ImageTk.PhotoImage(img)
    tk.Label(root, image=img, bg='white').place(x=50, y=50)

    frame = tk.Frame(root, width=500, height=500, bg="white")
    frame.place(relx=0.75, rely=0.5, anchor="center")

    def show_sign_in():
        for widget in frame.winfo_children():
            widget.destroy()

        heading = tk.Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 30, 'bold'))
        heading.place(x=130, y=10)

        user = create_placeholder_entry(frame, "Username", 50, 100)
        password = create_placeholder_entry(frame, "Password", 50, 180, show="*")

        user_error_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        user_error_label.place(x=50, y=140)

        password_error_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        password_error_label.place(x=50, y=220)

        add_eye_icon(frame, password, 410, 180)

        frame.bind("<Return>", lambda event: on_login())

        login_message_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        login_message_label.place(x=40, y=220)

        def on_login():
            user_error_label.config(text="")
            password_error_label.config(text="")
            login_message_label.config(text="")

            if user.get() == "" or user.get() == "Username":
                user_error_label.config(text="Please enter a username.")
                return
            if password.get() == "" or password.get() == "Password":
                password_error_label.config(text="Please enter a password.")
                return

            if validate_login(user.get(), password.get()):
                save_to_dataset(user.get(), password.get())
                execute_index2(root)
            else:
                login_message_label.config(text="Incorrect username or password.", fg="red")

        tk.Button(frame, text="Login", fg="white", bg="#57a1f8", font=('Microsoft YaHei UI Light', 10),
                  command=on_login, width=20, height=2).place(x=165, y=280)

        tk.Button(frame, text="Create User", fg="white", bg="#57a1f8", font=('Microsoft YaHei UI Light', 10),
                  command=show_create_user, width=20, height=2).place(x=165, y=340)

    def create_placeholder_entry(frame, placeholder, x, y, show=None):
        entry = tk.Entry(frame, width=30, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 14), show=show)
        entry.place(x=x, y=y)
        entry.insert(0, placeholder)

        tk.Frame(frame, width=400, height=3, bg='black').place(x=x, y=y+30)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        entry.config(fg="gray")
        return entry

    def show_create_user():
        for widget in frame.winfo_children():
            widget.destroy()

        heading = tk.Label(frame, text='Create User', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 30, 'bold'))
        heading.place(x=100, y=10)

        user = create_placeholder_entry(frame, "Username", 50, 100)
        password = create_placeholder_entry(frame, "Password", 50, 180, show="*")
        confirm_password = create_placeholder_entry(frame, "Confirm Password", 50, 260, show="*")

        password_error_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        password_error_label.place(x=50, y=300)
        confirm_password_error_label = tk.Label(frame, text="", fg="red", bg="white", font=('Microsoft YaHei UI Light', 12))
        confirm_password_error_label.place(x=60, y=300)

        add_eye_icon(frame, password, 410, 180)
        add_eye_icon(frame, confirm_password, 410, 260)

        create_user_message_label = tk.Label(frame, text="", fg="green", bg="white", font=('Microsoft YaHei UI Light', 12))
        create_user_message_label.place(x=50, y=300)

        def on_submit():
            password_error_label.config(text="")
            confirm_password_error_label.config(text="")
            create_user_message_label.config(text="")

            if user.get() == "" or user.get() == "Username":
                password_error_label.config(text="Please enter a username.")
                return
            if password.get() == "" or password.get() == "Password":
                password_error_label.config(text="Please enter a password.")
                return
            if confirm_password.get() == "" or confirm_password.get() == "Confirm Password":
                confirm_password_error_label.config(text="Please confirm your password.")
                return

            if password.get() != confirm_password.get():
                confirm_password_error_label.config(text="Passwords do not match!")
                return

            if create_user(user.get(), password.get()):
                show_sign_in()
            else:
                create_user_message_label.config(text="Username already exists.", fg="red")

        tk.Button(frame, text="Submit", fg="white", bg="#57a1f8", font=('Microsoft YaHei UI Light', 10),
                  command=on_submit, width=20, height=2).place(x=165, y=330)

        tk.Button(frame, text="Back to Login", fg="white", bg="#57a1f8", font=('Microsoft YaHei UI Light', 10),
                  command=show_sign_in, width=20, height=2).place(x=165, y=390)

        frame.bind("<Return>", lambda event: on_submit())

    show_sign_in()
    root.mainloop()

def add_eye_icon(frame, entry, x, y):
    eye_open = Image.open(eye_open_path).resize((20, 20))
    eye_open = ImageTk.PhotoImage(eye_open)

    eye_close = Image.open(eye_close_path).resize((20, 20))
    eye_close = ImageTk.PhotoImage(eye_close)

    show_password = False

    def toggle_password():
        nonlocal show_password
        if show_password:
            entry.config(show="*")
            eye_icon.config(image=eye_close)
        else:
            entry.config(show="")
            eye_icon.config(image=eye_open)
        show_password = not show_password

    eye_icon = tk.Button(frame, image=eye_close, bg="white", bd=0, command=toggle_password)
    eye_icon.place(x=x, y=y)

def execute_index2(root):
    for widget in root.winfo_children():
        widget.destroy()
    from index2 import SignLanguageApp
    app = SignLanguageApp(root, os.getcwd())  # Pass current directory as base

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg="#fff")
    root.resizable(False, False)
    setup_database()
    show_logo(root)
