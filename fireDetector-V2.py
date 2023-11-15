import cv2
import numpy as np
import time

# Initialize variables
Fire_Reported = False
min_area_threshold = 15000
max_area_threshold = 500000

def detect_fire(frame):
    # Apply Gaussian Blur for noise reduction
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Define lower and upper HSV thresholds for fire color
    lower = np.array([20, 100, 100])
    upper = np.array([60, 255, 255])

    # Create a mask to isolate fire color
    mask = cv2.inRange(hsv, lower, upper)

    # Apply morphological operations for noise reduction
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask

# Initialize video capture from webcam
video = cv2.VideoCapture(0)

while True:
    
    # Capture a frame from the webcam
    grabbed, frame = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540))

    # Detect fire regions
    fire_mask = detect_fire(frame)

    # Find contours in the mask
    contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Reset fire detection
    if Fire_Reported:
        Fire_Reported = False

    # Loop over the contours
    for contour in contours:
        area = cv2.contourArea(contour)
        print(f"Current Contour Area: {area}")

        if min_area_threshold < area < max_area_threshold:
            # Draw bounding box around detected fire
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            Fire_Reported = True

    if Fire_Reported:
        cv2.putText(frame, "FIRE DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("Fire Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
