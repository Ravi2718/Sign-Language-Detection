# login.py

import tkinter as tk

def create_login_page():
    # Create the main window for the login page
    root = tk.Tk()

    # Make the window fullscreen
    root.attributes('-fullscreen', True)

    # Set the background color to a light grey
    root.configure(bg="#f0f0f0")

    # Add a label for the title (Login Page)
    title_label = tk.Label(root, text="Login Page", font=("Helvetica", 30, "bold"), bg="#f0f0f0")
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # Add a label for the username input
    username_label = tk.Label(root, text="Username", font=("Helvetica", 20), bg="#f0f0f0")
    username_label.place(relx=0.5, rely=0.3, anchor="center")

    # Add an entry widget for the username
    username_entry = tk.Entry(root, font=("Helvetica", 18), width=20)
    username_entry.place(relx=0.5, rely=0.35, anchor="center")

    # Add a label for the password input
    password_label = tk.Label(root, text="Password", font=("Helvetica", 20), bg="#f0f0f0")
    password_label.place(relx=0.5, rely=0.45, anchor="center")

    # Add an entry widget for the password
    password_entry = tk.Entry(root, font=("Helvetica", 18), width=20, show="*")
    password_entry.place(relx=0.5, rely=0.5, anchor="center")

    # Function to handle login attempt
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        # You can add your authentication logic here
        if username == "admin" and password == "password":  # This is just an example.
            print("Login Successful!")
            root.destroy()  # Close the login window
            open_dashboard()  # Open the next page (dashboard)
        else:
            print("Login Failed!")
    
    # Add a button to submit the login
    login_button = tk.Button(root, text="Login", font=("Helvetica", 20), bg="#4CAF50", fg="white", command=handle_login)
    login_button.place(relx=0.5, rely=0.6, anchor="center")

    # Run the login page
    root.mainloop()

def open_dashboard():
    # Open the next page, like a dashboard or home page
    print("Dashboard or next page opens here")

# Run the login page
create_login_page()
