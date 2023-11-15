import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)  # Set the frame rate to 30 frames per second (adjust as needed)


while True:
    # Capture frames
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization
    gray = cv2.equalizeHist(gray)

    # Apply thresholding
    lower_bound = np.array([0, 0, 200])
    upper_bound = np.array([50, 50, 255])
    mask = cv2.inRange(frame, lower_bound, upper_bound)

    # Detect fire areas
    fire_image = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the result
    cv2.imshow('Fire Detection', fire_image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and clean up
cap.release()
cv2.destroyAllWindows()
