import os
import cv2
import shutil
import mediapipe as mp

# Set up MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize Mediapipe Hands
hands = mp_hands.Hands(
    static_image_mode=False,  # For live camera feed
    max_num_hands=2,  # Detect up to 2 hands
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

# Set up the data directory
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

dataset_size = 500  # Number of images to capture for each class
padding = 50  # Padding around the hand in the crop

# Initialize webcam
cap = cv2.VideoCapture(0)  # Default camera
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

def capture_images_for_class(folder_path, dataset_size):
    """Capture and save images for both hands detected together."""
    counter = 0
    while counter < dataset_size:
        success, frame = cap.read()
        if not success:
            print("Error: Failed to capture frame.")
            break

        frame = cv2.flip(frame, 1)  # Always flip the camera horizontally
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            # Initialize bounding box values for both hands
            x_min, y_min, x_max, y_max = float('inf'), float('inf'), -float('inf'), -float('inf')

            # Draw landmarks and calculate bounding box for all detected hands
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw the hand landmarks
                mp_drawing.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Get bounding box from landmarks
                for landmark in hand_landmarks.landmark:
                    img_h, img_w, _ = frame.shape
                    x, y = int(landmark.x * img_w), int(landmark.y * img_h)
                    x_min, y_min = min(x_min, x), min(y_min, y)
                    x_max, y_max = max(x_max, x), max(y_max, y)

            # Add padding to the bounding box
            x_min -= padding
            y_min -= padding
            x_max += padding
            y_max += padding

            # Ensure bounding box is within image boundaries
            x_min = max(x_min, 0)
            y_min = max(y_min, 0)
            x_max = min(x_max, frame.shape[1])
            y_max = min(y_max, frame.shape[0])

            # Crop the region containing both hands
            img_crop = frame[y_min:y_max, x_min:x_max]

            # Save the cropped image to the folder
            cv2.imwrite(os.path.join(folder_path, f'{counter}_both_hands.jpg'), img_crop)

            # Increment counter
            counter += 1

            # Display "Capturing..." message
            cv2.putText(frame, 'Capturing...', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Show the frame
        cv2.imshow("frame", frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    print(f"Captured {counter} images for class {folder_path}.")

while True:
    print("\nChoose an option:")
    print("1. Add a new folder(s).")
    print("2. Use an existing folder (override).")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == '1':
        # Add a new folder(s)
        try:
            num_classes = int(input("Enter the number of new classes: ").strip())
            if num_classes <= 0:
                print("Please enter a valid positive number.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        for i in range(num_classes):
            folder_name = input(f"Enter the name for class {i + 1}: ").strip()
            folder_path = os.path.join(DATA_DIR, folder_name)
            if os.path.exists(folder_path):
                print(f"Class folder '{folder_name}' already exists. Please choose a different name.")
                continue
            os.makedirs(folder_path)
            print(f'Collecting data for class "{folder_name}"...')

            # Wait for user input to start capturing
            while True:
                success, frame = cap.read()
                frame = cv2.flip(frame, 1)  # Flip camera feed horizontally
                cv2.putText(frame, 'Ready? Press "Q" to start capturing...', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('frame', frame)
                if cv2.waitKey(25) == ord('q'):
                    break

            # Start capturing images for the current class
            capture_images_for_class(folder_path, dataset_size)

        break

    elif choice == '2':
        # Use an existing folder
        folder_name = input("Enter the folder name to override: ").strip()
        folder_path = os.path.join(DATA_DIR, folder_name)
        if not os.path.exists(folder_path):
            print(f"Error: Folder '{folder_name}' does not exist.")
            continue
        # Clear folder contents directly
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' has been reset.")

        print(f'Collecting data for class "{folder_name}"...')
        while True:
            success, frame = cap.read()
            frame = cv2.flip(frame, 1)  # Flip camera feed horizontally
            cv2.putText(frame, 'Ready? Press "Q" to start capturing...', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            if cv2.waitKey(25) == ord('q'):
                break

        # Start capturing images for the current class
        capture_images_for_class(folder_path, dataset_size)

        break

    else:
        print("Invalid choice. Please enter 1 or 2.")

# Release resources and close the window
cap.release()
cv2.destroyAllWindows()
