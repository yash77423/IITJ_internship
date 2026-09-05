import cv2

video_path = "/home/birdlab1/Downloads/wolf.mp4"
cap = cv2.VideoCapture(video_path)

# Screen resolution (adjust if needed)
screen_width = 1280
screen_height = 720

if not cap.isOpened():
    print("❌ Error: Cannot open video")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("✅ End of video")
        break

    h, w = frame.shape[:2]

    # Compute scaling factor
    scale = min(screen_width / w, screen_height / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(frame, (new_w, new_h))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Video", resized)
    cv2.imshow("Grayscale", gray)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
