import cv2
import socket
import struct
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="Stream webcam to Ubuntu over TCP")
    parser.add_argument("--ip", type=str, required=True, help="IP address of the Ubuntu machine")
    parser.add_argument("--port", type=int, default=5005, help="Port to connect to (default: 5005)")
    args = parser.parse_args()

    print(f"Connecting to {args.ip}:{args.port}...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((args.ip, args.port))
        print("Connected successfully!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    print("Streaming started. Press Ctrl+C to stop.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Encodes frame to JPEG
            result, frame_encoded = cv2.imencode('.jpg', frame, encode_param)
            data = frame_encoded.tobytes()
            
            # Sends message size first, followed by data
            message_size = struct.pack(">L", len(data))
            client_socket.sendall(message_size + data)
            
            # Small delay to cap framerate at ~30fps
            time.sleep(0.033)
            
    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")
    except Exception as e:
        print(f"\nConnection lost: {e}")
    finally:
        cap.release()
        client_socket.close()

if __name__ == '__main__':
    main()
