import cv2 as cv
import numpy as np
import time


def detect_humans(frame):
    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
    person_detected = bool(len(rects) > 0)

    if person_detected:
        for (x, y, w, h) in rects:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, "Intruder Alert: Step Away for Cloak Activation", (x, y - 7), 
                       cv.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), thickness=1)

    return frame, person_detected


def capture_background(capture):
    global background, background_captured
    print("Looking for any jinx in the background...✨")

    for i in range(1, 50):
        ret, frame = capture.read()
        if not ret:
            break

        loading = "-" * i
        cv.putText(frame, str("Looking for Jinx"), (10, 30), 
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        cv.putText(frame, loading, (10, 50), 
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        
        cv.imshow("Invisibility Cloak Authentication", frame)
        cv.waitKey(25)

    # Gives Muggles time to exit frame completely
    # before capturing background
    # (50 iterations worth of time)
    ret, frame = capture.read()
    if ret:
        # Check if humans are still present in the frame
        _, person_detected = detect_humans(frame)
        if not person_detected and not background_captured:
            background = frame.copy()  # Capture the actual background
            background_captured = True
            print("Background captured! ✅")
            cv.imshow("Background", background)
        else:
            background_captured = False
            background = None
            print("Jinx detected ⚠️ Muggles exit frame!")
    return True


def authenticate_cloak(capture):
    # print("Authenticating...✨")

    for i in range(1, 50):
        ret, frame = capture.read()
        if not ret:
            break

        loading = "-" * i
        cv.putText(frame, str("Is your cloak truly enchanted?"), (10, 30), 
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        cv.putText(frame, loading, (10, 50), 
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        
        cv.imshow("Invisibility Cloak Authentication", frame)
        cv.waitKey(50)

    ret, frame = capture.read()

    if ret:
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        half_width, half_height = width // 4, height // 4

        cloak_region = frame[center_y - half_height:center_y + half_height, center_x - half_width:center_x + half_width]

        # Gathering Average color of ROI (Cloak Region)
        avg_color_per_channel = np.mean(cloak_region, axis=(0, 1)) 
        cloak = tuple(map(int, avg_color_per_channel))

        # Set cloak_authenticated to True after successful authentication
        global cloak_authenticated
        cloak_authenticated = True 

    return True

def disappear(capture):
    ret, frame = capture.read()
    if ret:
        print(cloak)
        cv.imshow("Invisibility Cloak - Get ready to disappear!", frame)

# Initialize HOG descriptor
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

# Open video capture
capture = cv.VideoCapture(0)
time.sleep(2)

background_captured = False
background = None
cloak_authenticated = False
cloak_region = None
cloak = None

while True:
    ret, frame = capture.read()
    if not ret:
        break  # No image was captured

    cv.putText(frame, "Press Esc to exit", (10, frame.shape[0] - 10), 
               cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), thickness=1)

    if not background_captured:
        # Step 1: Ask the person to step away and detect any human in the frame
        frame, person_detected = detect_humans(frame)

        if person_detected:
            print("Intruder Alert: Step Away for Cloak Activation")
        else:
            # Step 2: If no person is detected, capture the background
            capture_background(capture)
    else:
        if not cloak_authenticated: 
            # Step 5: Once the background is captured, prompt the user to display the cloak
            cv.putText(frame, "Authenticate Cloak \nIs your invisibility cloak authentic? Hold it up and let’s perform a magical verification!",
                       (10, 30), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), thickness=1)
            print("Does your cloak shimmer with pure magic✨?\nIf it shows too many colors, it may NOT possess the power of true invisibility. \nHold it steady, and let us confirm its authenticity.")

            authenticate_cloak(capture)

        else:
            disappear(capture)
        
    cv.imshow("Invisibility Cloak - Get ready to disappear!", frame)

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # Esc key
        break

capture.release()
cv.destroyAllWindows()
