import cv2
import os
import speech_recognition as sr

# Define the path to your video folder (relative to this script's directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
video_folder = os.path.join(BASE_DIR, "Transulator")

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
    cv2.moveWindow("Video", 1000, 500)  # Optional: position on screen

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (300, 300))  # Resize frame
        cv2.imshow("Video", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition.")
        return None

# Main Loop
if __name__ == "__main__":
    while True:
        spoken_text = recognize_speech()
        if spoken_text:
            play_video(spoken_text)
