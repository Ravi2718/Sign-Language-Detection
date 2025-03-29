import cv2
import os
import speech_recognition as sr

# Define the path to your video folder
video_folder = r"E:\SNS IT\final project\NSLD\Transulator"

def play_video(video_name):
    video_path = os.path.join(video_folder, video_name + ".mp4")

    if not os.path.exists(video_path):
        print(f"Video '{video_name}.mp4' not found!")
        return
    
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video '{video_name}.mp4'")
        return

    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    
    # Move the window to the bottom-right corner (adjust X, Y as needed)
    cv2.moveWindow("Video", 1000, 500)

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Stop when the video ends
        
        # Resize the frame to a small size (adjust as needed)
        frame = cv2.resize(frame, (300, 300))

        # Show the video in a separate window
        cv2.imshow("Video", frame)

        # Break when 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()  # Ensures all windows close

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds max
            text = recognizer.recognize_google(audio).lower()  # Convert to lowercase
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition.")
        return None

# Main Loop
while True:
    spoken_text = recognize_speech()
    if spoken_text:
        play_video(spoken_text)  # Try playing the video with the spoken word as the filename
