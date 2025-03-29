# import turtle
# import colorsys

# t = turtle.Turtle()
# screen = turtle.Screen()
# turtle.colormode(255)  # Enable RGB color mode

# t.speed(0)
# t.width(50)
# t.up()
# t.goto(0, 100)
# t.down()

# h = 0
# t.hideturtle()

# for i in range(20000):
#     r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(h, 1, 1)]
#     t.color(r, g, b)
#     t.circle(-100, 6)
#     h += 0.003
import os
import subprocess

def on_video_call_click():
    print("Video call icon clicked. Running Test.py...")
    try:
        # Use the full path to Test.py
        subprocess.run(["python", r"E:\SNS IT\final project\NSLD\Test.py"])
        print("Test.py executed successfully.")
    except Exception as e:
        print(f"Error running Test.py: {e}")