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
            print("Background captured! ✅")
            cv.imshow("Background", background)
        else:
            background_captured = False
            background = None
            print("Jinx detected ⚠️ Muggles exit frame!")
    return True


def authenticate_cloak(capture):
    global cloak_authenticated, cloak  

    for i in range(1, 50):
        ret, frame = capture.read()
        if not ret:
            break

        loading = "-" * i
        cv.putText(frame, str("Is your cloak truly enchanted?"), (10, 30), 
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        cv.putText(frame, loading, (10, 50), 
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), thickness=1)
        
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

        # Gathering Average color of ROI (Cloak Region)
        avg_color_per_channel = np.mean(cloak_region, axis=(0, 1)) 
        cloak = tuple(map(int, avg_color_per_channel))

        # Print debug information about the captured cloak color
        print(f"Captured cloak color (avg RGB): {cloak}")

        # Set cloak_authenticated to True after successful authentication
        cloak_authenticated = True 
        print(f"Cloak authentication successful -- {cloak}")

    return True


def disappear(capture):
    global cloak, background
    ret, frame = capture.read()
    if ret:
        if cloak is None or background is None:
            print("Cloak or background has not been authenticated or is None!")
            return
        else:
            # Convert frame to HSV
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            # Define cloak color range with a wider tolerance
            lower_bound = np.array([cloak[0] - 20, 100, 100])  # Adjust as necessary
            upper_bound = np.array([cloak[0] + 20, 255, 255])

            # Print the bounds for debugging
            print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")

            # Mask of cloak (detecting the cloak region based on color)
            mask = cv.inRange(hsv, lower_bound, upper_bound)
            
            # Mask of everything apart from Cloak (inverse mask)
            inverse_mask = cv.bitwise_not(mask)

            # Extract the cloak region from the current frame
            TheCloak = cv.bitwise_and(frame, frame, mask=mask)

            # Extract the background region where the cloak is present
            TheBackground = cv.bitwise_and(background, background, mask=mask)
            cv.imshow("TheBackround", TheBackground)

            # Extract everything apart from the cloak from the current frame
            RestOfTheFrame = cv.bitwise_and(frame, frame, mask=inverse_mask)
            cv.imshow("RestOfTheFrame", RestOfTheFrame)

            # Combine the RestOfTheFrame with the cloak-replaced background
            MagicFrame = cv.add(RestOfTheFrame, TheBackground)

            # Optional: Blur the edges for a smoother transition
            MagicFrame = cv.GaussianBlur(MagicFrame, (15, 15), 0)

            # Display the resulting frame
            cv.putText(MagicFrame, "Press Esc to exit", (10, frame.shape[0] - 10), 
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
