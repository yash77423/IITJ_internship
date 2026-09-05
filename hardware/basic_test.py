import cv2
import serial
import time

# =====================================
# SERIAL CONNECTION
# =====================================
ser = serial.Serial('COM6', 9600)

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
    # MOTION DETECTION
    # ---------------------------------
    diff = cv2.absdiff(frame1, frame2)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(
        blur,
        20,
        255,
        cv2.THRESH_BINARY
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detected = False

    display_frame = frame1.copy()

    # ---------------------------------
    # OBJECT DETECTION
    # ---------------------------------
    for contour in contours:

        area = cv2.contourArea(contour)

        if area > AREA_THRESHOLD:

            detected = True

            x, y, w, h = cv2.boundingRect(contour)

            # Bounding Box
            cv2.rectangle(
                display_frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Detection Label
            cv2.putText(
                display_frame,
                "OBJECT DETECTED",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # =====================================
    # SERIAL COMMANDS
    # =====================================

    # OBJECT DETECTED
    if detected:

        cv2.putText(
            display_frame,
            "MOTOR: ON",
            (20, 40),
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
            (20, 40),
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
        "DG2RL Object Detection",
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