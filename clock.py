import cv2 as cv
import numpy as np
import threading
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


def capture_background(frame):
    global background, background_captured
    print("Press Enter to capture the background...")
    
    while True:
        cv.imshow("Invisibility Cloak Authentication", frame)  # Show the current frame
        key = cv.waitKey(1) & 0xFF
        
        if key == 13:  # Enter key
            if capture_event.is_set():  # Check if the event is set (indicating shutdown)
                return
            if not background_captured:
                background = frame.copy()
                background_captured = True
                print("Background captured! ✅")
                cv.imshow("Background", background)
                break  # Exit the loop after capturing the background
        elif key == 27:  # Esc key
            capture_event.set()  # Set the event to signal the thread to stop
            break


# Event to control the thread's execution
capture_event = threading.Event()

# Initialize HOG descriptor
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

# Open video capture
capture = cv.VideoCapture(0)
time.sleep(5)

background_captured = False
background = None
background_thread = None

while True:
    ret, frame = capture.read()
    if not ret:
        break  # No image was captured

    cv.putText(frame, "Press Esc to exit", (10, frame.shape[0] - 10), 
               cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), thickness=1)

    # Only call detect_humans if the background is not captured
    if not background_captured:
        frame, person_detected = detect_humans(frame)

        if person_detected:
            print("Intruder Alert: Step Away for Cloak Activation")
            background_captured = False  # Reset background capture if a person is detected
        else:
            cv.putText(frame, "No human detected. Press Enter to capture background...", (10, 30), 
                       cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), thickness=1)

            # Start a thread to capture the background if Enter is pressed
            if background_thread is None or not background_thread.is_alive():
                background_thread = threading.Thread(target=capture_background, args=(frame,))
                background_thread.start()

    cv.imshow("Invisibility Cloak Authentication", frame)

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # Esc key
        capture_event.set()  # Set the event to signal the thread to stop
        break

# Wait for the background capture thread to finish
if background_thread is not None:
    background_thread.join()

capture.release()
cv.destroyAllWindows()
