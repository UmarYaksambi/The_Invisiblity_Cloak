import cv2 as cv
import numpy as np
import time


def detect_humans(frame):
    (rects, _) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
    person_detected = len(rects) > 0

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
        cv.putText(frame, "Looking for Jinx", (10, 30), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        cv.putText(frame, loading, (10, 50), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        cv.imshow("Invisibility Cloak - Get ready to disappear!", frame)
        cv.waitKey(60)

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
            print("No jinx found in the Background ✅")
            bg_hsv = cv.cvtColor(background, cv.COLOR_BGR2HSV)
            return True
        else:
            background_captured = False
            background = None
            print("Jinx detected ⚠️ Muggles exit frame!")
            return False


def authenticate_cloak(capture):
    global cloak_authenticated, cloak  

    for i in range(1, 50):
        ret, frame = capture.read()
        if not ret:
            break

        loading = "-" * i
        cv.putText(frame, "Is your cloak truly enchanted?", (10, 30), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        cv.putText(frame, loading, (10, 50), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        cv.imshow("Invisibility Cloak - Get ready to disappear!", frame)
        cv.waitKey(60)

    ret, frame = capture.read()

    if ret:
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        half_width, half_height = width // 4, height // 4

        cloak_region = frame[center_y - half_height:center_y + half_height, center_x - half_width:center_x + half_width]

        if cloak_region.size == 0:
            print("Cloak region is empty or invalid!")
            return False

        # Convert the cloak region to HSV
        cloak_hsv = cv.cvtColor(cloak_region, cv.COLOR_BGR2HSV)

        # Gathering Average color of ROI (Cloak Region)
        cloak = tuple(map(int, np.mean(cloak_hsv, axis=(0, 1))))

        # Set cloak_authenticated to True after successful authentication
        cloak_authenticated = True 
        print(f"Cloak authentication successful ---- {cloak}")
        CloakFrame = np.full((100, 100, 3), cloak, dtype=np.uint8)
        CloakFrame = cv.cvtColor(CloakFrame, cv.COLOR_HSV2BGR)  # Convert back to BGR for display
        cv.imshow("Cloak Authenticated", CloakFrame)

    return True


def disappear(capture):
    global cloak, background
    ret, frame = capture.read()
    if ret:
        if cloak is None or background is None:
            print("Cloak or background has not been authenticated or is None!")
            return
        # Convert frame to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # Define cloak color range with a wider tolerance
        lower_bound = np.array([cloak[0] - 10, 50, 50])   # Adjust to fine tune
        upper_bound = np.array([cloak[0] + 10, 255, 255])

        # Mask of cloak (detecting the cloak region based on color)
        mask = cv.inRange(hsv, lower_bound, upper_bound)
            
        # Mask of everything apart from Cloak (inverse mask)
        inverse_mask = cv.bitwise_not(mask)

        TheBackground = cv.bitwise_and(background, background, mask=mask)
        RestOfTheFrame = cv.bitwise_and(frame, frame, mask=inverse_mask)
        MagicFrame = cv.add(TheBackground, RestOfTheFrame)
        
        # MagicFrame = cv.GaussianBlur(MagicFrame, (15, 15), 0)
        # Need to refine blur for just edges

        cv.putText(MagicFrame, "Press Esc to exit ---", (10, frame.shape[0] - 10),
                   cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), thickness=1)
        cv.imshow("Invisibility Cloak - Get ready to disappear!", MagicFrame)


# Initialize HOG descriptor
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

# Open video capture
capture = cv.VideoCapture(0)
time.sleep(2)

background_captured = False
background = None
cloak_authenticated = False
cloak = None


while True:   # Main Loop
    ret, frame = capture.read()
    if not ret:
        break

    cv.putText(frame, "Press Esc to exit", (10, frame.shape[0] - 10), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), thickness=1)

    if not background_captured:   # Capture Background
        frame, person_detected = detect_humans(frame)   # Muggles and creatures must step out of frame
        if person_detected:
            print("Intruder Alert: Step Away for Cloak Activation")
        else:
            capture_background(capture)
    else:
        if not cloak_authenticated:   # Capture Cloak
            cv.putText(frame, "Authenticate Cloak\nHold it up and let’s perform a magical verification!",
                       (10, 30), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), thickness=1)
            authenticate_cloak(capture)
        else:
            disappear(capture)   # Disappear with the Cloak

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # Esc key
        break

capture.release()
cv.destroyAllWindows()
