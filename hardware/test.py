import cv2
import numpy as np
import serial
import time

# =====================================
# SERIAL CONNECTION
# =====================================
ser = serial.Serial('COM7', 9600)

time.sleep(2)

# =====================================
# CAMERA SETUP
# =====================================
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

# =====================================
# PARAMETERS
# =====================================
AREA_THRESHOLD = 3000

last_state = "0"

# =====================================
# MAIN LOOP
# =====================================
while True:

    # ---------------------------------
    # GAP DETECTION
    # ---------------------------------
    detected = False
    display_frame = frame1.copy()

    hsv = cv2.cvtColor(display_frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))
    mask2 = cv2.inRange(hsv, np.array([160, 50, 50]), np.array([180, 255, 255]))
    red_mask = cv2.bitwise_or(mask1, mask2)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid_contours = [c for c in contours if cv2.contourArea(c) > 500] 
    if len(valid_contours) >= 2:
        sorted_contours = sorted(valid_contours, key=lambda c: cv2.boundingRect(c)[0])
        left_contour = sorted_contours[0]
        right_contour = sorted_contours[-1]

        x1, _, w1, _ = cv2.boundingRect(left_contour)
        x2, _, w2, _ = cv2.boundingRect(right_contour)

        gap_width_pixels = x2 - (x1 + w1)

        # Draw visual markers on the frame for the user
        cv2.rectangle(display_frame, (x1, 0), (x1+w1, 480), (0, 0, 255), 2)
        cv2.rectangle(display_frame, (x2, 0), (x2+w2, 480), (0, 0, 255), 2)
        cv2.putText(display_frame, f"Gap: {gap_width_pixels}px", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        drone_arm_pixel_width = 250
        navigability_score = gap_width_pixels / drone_arm_pixel_width

        if navigability_score < 1.0:
            detected = True

    # =====================================
    # SERIAL COMMANDS
    # =====================================

    # OBJECT DETECTED
    if detected:

        cv2.putText(
            display_frame,
            "MOTOR: ON",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        if last_state != "1":

            ser.write(b'1')

            print("OBJECT DETECTED -> MOTOR ON")

            last_state = "1"

    # NO OBJECT
    else:

        cv2.putText(
            display_frame,
            "MOTOR: STOP",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            3
        )

        if last_state != "0":

            ser.write(b'0')

            print("NO OBJECT -> MOTOR STOP")

            last_state = "0"

    # =====================================
    # DISPLAY
    # =====================================
    cv2.imshow(
        "Gap Detection",
        display_frame
    )

    # Update frames
    frame1 = frame2

    ret, frame2 = cap.read()

    if not ret:
        break

    # ESC key to exit
    if cv2.waitKey(10) == 27:
        break

# =====================================
# CLEANUP
# =====================================
cap.release()

cv2.destroyAllWindows()

ser.close()