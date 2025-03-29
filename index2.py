import tkinter as tk
from tkinter import Label, Canvas
from PIL import Image, ImageTk, ImageDraw
import cv2
from threading import Thread, Lock
import subprocess
import turtle
import colorsys
import time
import os

class SignLanguageApp:
    def __init__(self, root, base_dir):
        self.root = root
        self.base_dir = base_dir  # Store the base directory
        self.video_playing = False  # Flag to track if a video is currently playing
        self.video_lock = Lock()  # Thread lock for video playback
        self.original_packing = {}  # Stores packing info for widgets to restore later
        self.image_references = []  # Stores references to images to prevent garbage collection
        self.main()  # Initialize the main UI

    def execute_test_script(self, event):
        """
        Executes the Test.py script and displays turtle graphics animation.
        """
        self.hide_all_widgets()  # Hide all widgets to make space for the animation
        self.root.configure(bg="white")  # Set background color to white

        try:
            # Execute the Test.py script in a subprocess
            subprocess.Popen(["python", os.path.join(self.base_dir, "Test.py")])
        except Exception as e:
            print(f"Error executing Test.py: {e}")

        # Create a canvas for turtle graphics
        canvas = tk.Canvas(self.root, bg="white")
        canvas.pack(fill="both", expand=True)
        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor("white")
        t = turtle.RawTurtle(screen)
        t.speed(0)
        t.width(50)
        t.up()
        t.goto(600, -200)
        t.down()
        h = 0
        t.hideturtle()

        def draw_turtle_graphics():
            """
            Draws a colorful turtle graphics animation for 15 seconds.
            """
            nonlocal h
            start_time = time.time()
            try:
                while time.time() - start_time < 15:
                    r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
                    t.color(r, g, b)
                    t.circle(-100, 6)
                    h += 0.003
                    self.root.update()
            finally:
                screen.clear()  # Clear the turtle graphics
                canvas.pack_forget()  # Remove the canvas from the window
                self.restore_all_widgets()  # Restore the original widgets

        # Run the turtle graphics animation in a separate thread
        Thread(target=draw_turtle_graphics).start()

    def hide_all_widgets(self):
        """
        Hides all widgets in the root window.
        """
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Label, tk.Button)):
                info = widget.pack_info()
                self.original_packing[widget] = info
                widget.pack_forget()

    def restore_all_widgets(self):
        """
        Restores all previously hidden widgets in the root window.
        """
        for widget, config in self.original_packing.items():
            widget.pack(**config)

    def main(self):
        """
        Main function to set up the UI for the sign language application.
        """
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Configure the root window
        self.root.title("Sign Language UI")
        self.root.configure(bg="white")

        # Define image and video pairs
        image_video_pairs = [
            {"image": os.path.join(self.base_dir, "image", "sign", "hello.jpg"), "video": os.path.join(self.base_dir, "Transulator", "sign video", "hello.mp4"), "text": "Hello"},
            {"image": os.path.join(self.base_dir, "image", "sign", "My.jpg"), "video": os.path.join(self.base_dir, "Transulator", "sign video", "My.mp4"), "text": "My"},
            {"image": os.path.join(self.base_dir, "image", "sign", "I love you.jpg"), "video": os.path.join(self.base_dir, "Transulator", "sign video", "I Love You.mp4"), "text": "I Love You"},
            {"image": os.path.join(self.base_dir, "image", "sign", "Food.jpg"), "video": os.path.join(self.base_dir, "Transulator", "sign video", "Food.mp4"), "text": "Food"}
        ]

        # Load images and prepare PhotoImage objects
        for pair in image_video_pairs:
            try:
                image = Image.open(pair["image"]).resize((300, 300), Image.Resampling.LANCZOS)
                pair["photo"] = ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"Error loading image {pair['image']}: {e}")
                pair["photo"] = None

        # Add a heading label
        heading_label = tk.Label(self.root, text="Common Sign Language", font=("Arial", 30, "bold"), bg="white", fg="black")
        heading_label.pack(pady=40)

        # Create a frame to hold the image and video pairs
        image_frame = tk.Frame(self.root, bg="white")
        image_frame.pack(pady=20)

        def play_video(video_path, label, original_image):
            """
            Plays a video in the specified label.
            """
            with self.video_lock:
                if self.video_playing:
                    return
                self.video_playing = True

            # Check if the video file exists
            if not os.path.exists(video_path):
                print(f"Error: Video file not found at {video_path}")
                with self.video_lock:
                    self.video_playing = False
                return

            # Open the video file
            cap = cv2.VideoCapture(video_path)
            try:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame = cv2.resize(frame, (300, 300))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=img)
                    label.config(image=imgtk)
                    label.image = imgtk
                    self.root.update()
            finally:
                cap.release()
                with self.video_lock:
                    self.video_playing = False
                label.config(image=original_image)
                label.image = original_image

        def on_image_click(event, video_path, original_image):
            """
            Handles click events on images to play videos.
            """
            video_label = event.widget
            Thread(target=play_video, args=(video_path, video_label, original_image)).start()

        # Add image and video pairs to the frame
        for pair in image_video_pairs:
            if pair["photo"] is None:
                continue

            pair_frame = tk.Frame(image_frame, bg="white")
            pair_frame.pack(side="left", padx=20, pady=10)

            image_label = tk.Label(pair_frame, image=pair["photo"], bg="white")
            image_label.image = pair["photo"]
            image_label.pack()
            image_label.bind("<Button-1>", lambda e, vp=pair["video"], img=pair["photo"]: on_image_click(e, vp, img))

            text_label = tk.Label(pair_frame, text=pair["text"], font=("Arial", 16), bg="white", fg="black")
            text_label.pack(pady=5)

        # Define paths for icons and profile images
        video_icon_path = os.path.join(self.base_dir, "image", "sign", "video call", "video.png")
        image_icon_path = os.path.join(self.base_dir, "image", "sign", "video call", "image.png")
        dropdown_icon_path = os.path.join(self.base_dir, "image", "sign", "video call", "chevron-down.png")
        profile_image_path = os.path.join(self.base_dir, "image", "sign", "video call", "image 1.png")
        background_path = os.path.join(self.base_dir, "image", "sign", "video call", "background.png")

        def load_image(path, size):
            """
            Loads and resizes an image from the specified path.
            """
            try:
                img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image from {path}: {e}")
                return None

        def create_rounded_rectangle(width, height, radius, color):
            """
            Creates a rounded rectangle image.
            """
            img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
            return ImageTk.PhotoImage(img)

        # Load icons and profile images
        profile_pic = load_image(profile_image_path, (50, 50))
        dropdown_icon = load_image(dropdown_icon_path, (20, 20))
        image_icon = load_image(image_icon_path, (30, 30))
        video_icon = load_image(video_icon_path, (30, 30))

        self.image_references.extend([profile_pic, dropdown_icon, image_icon, video_icon])

        def create_profile_card(frame, x_position, y_position, name, use_background=False):
            """
            Creates a profile card with a rounded rectangle background.
            """
            rounded_card = create_rounded_rectangle(600, 80, 20, "#0F4C5C")
            canvas = Canvas(frame, width=600, height=80, bg="white", highlightthickness=0)
            canvas.place(x=x_position, y=y_position)
            canvas.create_image(0, 0, anchor="nw", image=rounded_card)
            canvas.image = rounded_card

            if use_background:
                bg_image = load_image(background_path, (600, 80))
                if bg_image:
                    bg_label = tk.Label(frame, image=bg_image, bg="white")
                    bg_label.image = bg_image
                    bg_label.place(x=x_position, y=y_position)

            if profile_pic:
                profile_label = tk.Label(frame, image=profile_pic, bg="#0F4C5C")
                profile_label.place(x=x_position + 15, y=y_position + 15)

            name_label = tk.Label(frame, text=name, fg="white", bg="#0F4C5C", font=("Arial", 14, "bold"))
            name_label.place(x=x_position + 80, y=y_position + 25)

            if dropdown_icon:
                dropdown_label = tk.Label(frame, image=dropdown_icon, bg="#0F4C5C")
                dropdown_label.place(x=x_position + 410, y=y_position + 25)

            if image_icon:
                image_label = tk.Label(frame, image=image_icon, bg="#0F4C5C")
                image_label.place(x=x_position + 450, y=y_position + 20)

            if video_icon:
                video_label = tk.Label(frame, image=video_icon, bg="#0F4C5C")
                video_label.place(x=x_position + 500, y=y_position + 20)
                video_label.bind("<Button-1>", self.execute_test_script)

        # Create a frame for video call profiles
        video_call_frame = tk.Frame(self.root, bg="white")
        video_call_frame.pack(fill="both", expand=True, pady=0)

        # Add profile cards
        create_profile_card(video_call_frame, 100, 10, "Emma", use_background=True)
        create_profile_card(video_call_frame, 750, 10, "John Doe", use_background=True)
        create_profile_card(video_call_frame, 100, 100, "James", use_background=True)
        create_profile_card(video_call_frame, 750, 100, "Jane Smith", use_background=True)

        # Add an exit button
        exit_button = tk.Button(self.root, text="Exit Full Screen", command=self.root.destroy, font=("Arial", 14), bg="white", fg="black")
        exit_button.pack(pady=20)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    app = SignLanguageApp(root, BASE_DIR)
    root.mainloop()