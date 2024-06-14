import socket
import cv2
import pickle
import struct
import time
import argparse


def run():
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=str)
    args = parser.parse_args()
    video_path = args.video

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = 10050
    print('Host IP: ', host_ip)
    
    socket_address = (host_ip, port)
    print("Socket created")

    server_socket.bind(socket_address)
    print("Socket bind complete")

    server_socket.listen(5)
    print("Socket now listening")

    # stream video
    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from:", addr)

        if client_socket:
            vid = cv2.VideoCapture(video_path)
            while (vid.isOpened()):
                time.sleep(0.1)
                success, frame = vid.read()

                if success:
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

                    cv2.imshow("sending...", frame)
                    key = cv2.waitKey(10)
                    if key == 13:
                        client_socket.close()
        


if __name__ == "__main__":
    run()