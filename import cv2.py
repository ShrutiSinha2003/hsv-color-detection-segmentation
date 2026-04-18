import cv2
import numpy as np

def nothing(x):
    pass

# Create trackbar window
cv2.namedWindow("Trackbars")

# Lower HSV
cv2.createTrackbar("LH", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 0, 255, nothing)

# Upper HSV
cv2.createTrackbar("UH", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)

# Open webcam
cap = cv2.VideoCapture(0)

# Define video writer for saving
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_segment = cv2.VideoWriter('segmented_output.avi', fourcc, 20.0, (640, 480))
out_mask = cv2.VideoWriter('mask_output.avi', fourcc, 20.0, (640, 480), isColor=False)

img_count = 0  # for image filenames

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Trackbar values
    lh = cv2.getTrackbarPos("LH", "Trackbars")
    ls = cv2.getTrackbarPos("LS", "Trackbars")
    lv = cv2.getTrackbarPos("LV", "Trackbars")

    uh = cv2.getTrackbarPos("UH", "Trackbars")
    us = cv2.getTrackbarPos("US", "Trackbars")
    uv = cv2.getTrackbarPos("UV", "Trackbars")

    # Color range
    lower_hsv = np.array([lh, ls, lv])
    upper_hsv = np.array([uh, us, uv])

    # Mask and result
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Show
    cv2.imshow("Original", frame)
    cv2.imshow("Segmented", result)
    cv2.imshow("Mask", mask)

    # Save video frames
    out_segment.write(result)
    out_mask.write(mask)

    key = cv2.waitKey(1) & 0xFF

    # Press 's' to save images
    if key == ord('s'):
        cv2.imwrite(f"saved_segment_{img_count}.jpg", result)
        cv2.imwrite(f"saved_mask_{img_count}.jpg", mask)
        print(f"Saved frame {img_count}")
        img_count += 1

    # Press 'q' to quit
    if key == ord('q'):
        break

# Release everything
cap.release()
out_segment.release()
out_mask.release()
cv2.destroyAllWindows()


