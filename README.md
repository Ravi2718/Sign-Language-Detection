# NSLD - Sign Language Translator

## Overview
NSLD (Non-Speaking Language Detector) is an AI-powered sign language translator that utilizes **OpenCV**, **MediaPipe**, and **deep learning** to recognize hand gestures and convert them into text, speech, or corresponding videos.

## Features
- **User Authentication**: Secure login system with SQLite.
- **Hand Gesture Recognition**: Uses a trained deep learning model to recognize sign language.
- **Speech-to-Video Conversion**: Converts spoken words into sign language videos.
- **Text-to-Speech**: Speaks out detected gestures.
- **Video Call Interface**: Includes a video call GUI for communication.
- **Docker Support**: Can be containerized for deployment on different systems.

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/NSLD.git
cd NSLD
```

### 2. Install Dependencies
Ensure **Python 3.8+** is installed, then install required libraries:
```sh
pip install -r requirements.txt
```

### 3. Setup Database
```sh
python dataset.py
```
This initializes `dataset.sql` and sets up the user authentication system.

### 4. Running the Application
Run the main GUI:
```sh
python index.py
```

To start the **sign language detection module**:
```sh
python test.py
```

## Running as an EXE File
If you have the pre-built **EXE version**, simply **double-click** `NSLD.exe` to launch the program.

## Running with Docker
If you want to run the project inside a **Docker container**:
1. Install **Docker**.
2. Build the Docker image:
   ```sh
   docker build -t nsld .
   ```
3. Run the container:
   ```sh
   docker run -p 8000:8000 nsld
   ```

## Project Structure
```
NSLD/
│
├── dataset.py       # SQLite authentication system
├── index.py         # Login GUI
├── index2.py        # Sign language learning interface
├── test.py          # Sign language detection & translation
│
├── Model/           # Trained Keras model for gesture classification
├── Transulator/     # Sign language videos
├── image/           # Images for UI
├── Sound/           # Audio files
├── dataset.sql      # User credentials database
│
└── README.md        # This file
```

## 📽️ Project Demo

[![Watch the Demo](https://img.youtube.com/vi/ifynWNDr9j0/maxresdefault.jpg)](https://youtu.be/ifynWNDr9j0)


## Contributors
- **Your Name** - Developer
- **Other Contributors** - Additional team members

## License
This project is licensed under the **MIT License**.

