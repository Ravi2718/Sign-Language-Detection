import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class FrontPageApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration for full screen
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")  # Full screen
        self.title("Common Sign Language")
        self.configure(bg="white")
        self.resizable(False, False)  # Disable resizing the window

        # Title label at the top left
        self.title_label = tk.Label(self, text="Common Sign Language", font=("Helvetica", 20, "bold"), bg="white", anchor="w")
        self.title_label.place(x=10, y=10)

        # First two boxes for user input
        self.box1_label = tk.Label(self, text="Box 1:", font=("Helvetica", 12), bg="white")
        self.box1_label.place(x=10, y=80)
        self.box1 = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.box1.place(x=100, y=80)

        self.box2_label = tk.Label(self, text="Box 2:", font=("Helvetica", 12), bg="white")
        self.box2_label.place(x=10, y=120)
        self.box2 = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.box2.place(x=100, y=120)

        # Next two boxes further down
        self.box3_label = tk.Label(self, text="Box 3:", font=("Helvetica", 12), bg="white")
        self.box3_label.place(x=10, y=160)
        self.box3 = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.box3.place(x=100, y=160)

        self.box4_label = tk.Label(self, text="Box 4:", font=("Helvetica", 12), bg="white")
        self.box4_label.place(x=10, y=200)
        self.box4 = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.box4.place(x=100, y=200)

        # Video Call button at the bottom
        self.video_call_button = tk.Button(self, text="Video Call", font=("Helvetica", 14), bg="blue", fg="white", command=self.open_video_call)
        self.video_call_button.place(x=self.winfo_screenwidth() // 2 - 100, y=self.winfo_screenheight() - 100)

    def open_video_call(self):
        """Function to open and execute Test.py"""
        try:
            # Running Test.py (ensure that the path to Test.py is correct)
            subprocess.run(["python", "E:\\SNS IT\\project\\NSLD\\Test.py"], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open video call: {e}")
        
        # After running Test.py, quit the application (end task)
        self.quit()

if __name__ == "__main__":
    app = FrontPageApp()
    app.mainloop()
