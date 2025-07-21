import cv2
import numpy as np
import pyttsx3
import time
import os
import sys
import mediapipe as mp
import threading
import queue
import speech_recognition as sr
from playsound import playsound

# Suppress TensorFlow/Keras logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Suppress OpenCV output
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Base path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MediaPipe Hand Detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(max_num_hands=2)

# Import classifier
from cvzone.ClassificationModule import Classifier
classifier = Classifier(
    os.path.join(BASE_DIR, "Model", "keras_model.h5"),
    os.path.join(BASE_DIR, "Model", "labels.txt")
)

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Speech recognition setup
recognizer = sr.Recognizer()
recognized_text = ""
listening = False
stop_listening = False
last_speech_time = 0
speech_display_time = 3

# Speech queue
speech_queue = queue.Queue()

# Paths
video_folder = os.path.join(BASE_DIR, "Transulator")
sound_path = os.path.join(BASE_DIR, "Sound", "end_sound.mp3")
current_video_frame = None
video_playing = False

# Sound playback
def play_sound(sound_path):
    try:
        playsound(sound_path)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Video playback
def play_video(video_name):
    global current_video_frame, video_playing
    video_path = os.path.join(video_folder, video_name + ".mp4")

    if not os.path.exists(video_path):
        print(f"Video '{video_name}.mp4' not found!")
        return

    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print(f"Error: Could not open video '{video_name}.mp4'")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    desired_fps = 24
    delay = 1 / desired_fps
    video_playing = True

    while video_playing:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (200, 200))
        current_video_frame = frame
        time.sleep(delay)

    cap.release()
    video_playing = False
    current_video_frame = None

# Speech synthesis thread
def speak():
    while True:
        word = speech_queue.get()
        try:
            engine.say(word)
            engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

speech_thread = threading.Thread(target=speak, daemon=True)
speech_thread.start()

# Recognize speech while holding 'M'
def recognize_speech():
    global recognized_text, listening, stop_listening, last_speech_time
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        while listening:
            try:
                audio = recognizer.listen(source, timeout=None)
                text = recognizer.recognize_google(audio).lower()
                recognized_text = text
                last_speech_time = time.time()

                video_name = recognized_text
                video_path = os.path.join(video_folder, video_name + ".mp4")
                if os.path.exists(video_path):
                    threading.Thread(target=play_video, args=(video_name,), daemon=True).start()
                else:
                    print(f"Video '{video_name}.mp4' not found!")
            except sr.UnknownValueError:
                recognized_text = ""
            except sr.RequestError:
                recognized_text = "Speech service error"
            if stop_listening:
                break

# Configuration
offset = 20
imgSize = 300
labels = ["Hello", "YES", "NO", "Thank you"]
prev_word = ""
speak_delay = 2
last_speak_time = 0
voice_on = False
status_display_time = 1
status_last_shown_time = 0

# UI Window
cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Webcam capture
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    imgOutput = frame.copy()
    word = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                imgOutput,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * frame.shape[1])
            y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * frame.shape[0])
            x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * frame.shape[1])
            y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * frame.shape[0])

            imgCrop = frame[y_min - offset:y_max + offset, x_min - offset:x_max + offset]
            if imgCrop.size > 0:
                imgCrop = cv2.resize(imgCrop, (100, 100))
                imgOutput[20:120, imgOutput.shape[1] - 120:imgOutput.shape[1] - 20] = imgCrop

                prediction, index = classifier.getPrediction(imgCrop, draw=False)
                word = labels[index]

        text_x = (imgOutput.shape[1] - cv2.getTextSize(word, cv2.FONT_HERSHEY_COMPLEX, 1.7, 2)[0][0]) // 2
        text_y = imgOutput.shape[0] - 50
        cv2.putText(imgOutput, word, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 1.7,
                    (0, 255, 0) if voice_on else (0, 255, 255), 2)

        if voice_on and word != prev_word and (time.time() - last_speak_time > speak_delay):
            speech_queue.put(word)
            last_speak_time = time.time()
            prev_word = word

    if listening:
        cv2.putText(imgOutput, "Listening...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    if recognized_text and (time.time() - last_speech_time < speech_display_time):
        text_x = (imgOutput.shape[1] - cv2.getTextSize(recognized_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)[0][0]) // 2
        text_y = imgOutput.shape[0] - 100
        cv2.putText(imgOutput, recognized_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    if current_video_frame is not None:
        imgOutput[20:220, imgOutput.shape[1] - 220:imgOutput.shape[1] - 20] = current_video_frame

    cv2.imshow("Image", imgOutput)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('e'):
        voice_on = not voice_on
        status_last_shown_time = time.time()
        print(f"Voice {'ON' if voice_on else 'OFF'}")
    elif key == ord('m'):
        if not listening:
            listening = True
            stop_listening = False
            threading.Thread(target=play_sound, args=(sound_path,), daemon=True).start()
            speech_thread = threading.Thread(target=recognize_speech, daemon=True)
            speech_thread.start()
    elif key == -1 and listening:
        listening = False
        stop_listening = True

cap.release()
cv2.destroyAllWindows()
