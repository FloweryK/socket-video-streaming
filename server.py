import socket
import cv2
import pickle
import struct
import time
import argparse
from config import SERVER_HOST, SERVER_PORT


def stream_video(video_path):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (SERVER_HOST, SERVER_PORT)
    print(f"Host IP: {SERVER_HOST}")

    # Bind the socket to the address and port
    server_socket.bind(socket_address)
    print("Socket bind complete")

    # Listen for incoming connections
    server_socket.listen(5)
    print("Socket now listening")

    while True:
        # Wait for a connection
        client_socket, addr = server_socket.accept()
        print("Connection from:", addr)

        if client_socket:
            # Open the video file
            vid = cv2.VideoCapture(video_path)
            while vid.isOpened():
                time.sleep(0.1)
                success, frame = vid.read()

                if success:
                    # Serialize the frame
                    data = pickle.dumps(frame)

                    # Pack the frame size and data
                    message = struct.pack("Q", len(data)) + data

                    # Send data to the client
                    client_socket.sendall(message)

                    # Display the frame being sent
                    cv2.imshow("sending...", frame)
                    key = cv2.waitKey(10)

                    # Close the socket
                    if key == 13:
                        client_socket.close()
                        break

            # Release the video capture object
            vid.release()


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=str)
    args = parser.parse_args()

    # Start streaming video
    stream_video(args.video)


if __name__ == "__main__":
    main()
