import schedule
import time
import cv2
import os

# Configs
PHOTOS_COUNT = 0
INTERVAL = 5  # In seconds
X_TEXT_POS = 30
Y_TEXT_POS = 30
SAMPLE_ID = "give_a_id"
FONT_RGB = 0, 0, 0
PHOTOS_FOLDER = "give_a_name"
IS_WATERMARK = False  # True = On | Flase = Off
WEBCAM_ID = 0  # Change for different webcams. E.g.: 0 , 1 , 2...


def handle_project_folder():
    if not os.path.isdir(f"./{PHOTOS_FOLDER}/"):
        os.makedirs(f"./{PHOTOS_FOLDER}/")


def count_files():
    files_in_dir = 0
    for filename in os.listdir(f'./{PHOTOS_FOLDER}'):
        if filename.endswith('.png'):
            files_in_dir += 1
    return files_in_dir


def take_timestamp_photo():
    # Photo count verification
    global PHOTOS_COUNT
    if PHOTOS_COUNT == 0:
        PHOTOS_COUNT = count_files()
    # Webcam handling
    cap = cv2.VideoCapture(WEBCAM_ID)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    ret, frame = cap.read()
    # Timestamp
    if IS_WATERMARK:
        timestamp = str(time.strftime(f"%d/%m/%Y-%H:%M:%S, {SAMPLE_ID}"))
        font = cv2.FONT_HERSHEY_COMPLEX
        frame = cv2.putText(frame, timestamp, (X_TEXT_POS,
                            Y_TEXT_POS), font, 0.5, FONT_RGB, 1)
    # File saving
    filename = f'./{PHOTOS_FOLDER}/{str(PHOTOS_COUNT).zfill(3)}.png'
    PHOTOS_COUNT += 1
    cv2.imwrite(f"{filename}", frame)
    cap.release()


def main():
    handle_project_folder()
    # Queue function calling every interval
    schedule.every(interval=INTERVAL).seconds.do(take_timestamp_photo)
    # Check if needs to take photo every second
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
