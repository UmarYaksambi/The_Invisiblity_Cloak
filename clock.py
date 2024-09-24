import cv2 as cv
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

    for i in range(1, 40):
        ret, frame = capture.read()  # Fetch a new frame in each loop iteration
        if not ret:
            break

        text = "Looking for Jinx " + "-" * i
        cv.putText(frame, text, (10, 30), 
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        
        cv.imshow("Invisibility Cloak Authentication", frame)
        cv.waitKey(50)

    # Once the loading finishes (after 100 iterations), capture the background
    ret, frame = capture.read()  # Fetch a final frame to capture the background
    if ret and not background_captured:
        background = frame.copy()
        background_captured = True
        print("Background captured! ✅")
        cv.imshow("Background", background)
    return True


# Initialize HOG descriptor
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

# Open video capture
capture = cv.VideoCapture(0)
time.sleep(2)

background_captured = False
background = None

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
        # Step 5: Once the background is captured, prompt the user to display the clock
        cv.putText(frame, "Next Step! ", (10, 30), 
                   cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), thickness=1)

    cv.imshow("Invisibility Cloak Authentication", frame)

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # Esc key
        break

capture.release()
cv.destroyAllWindows()
