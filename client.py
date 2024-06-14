import socket
import cv2
import pickle
import struct
from config import SERVER_HOST, SERVER_PORT


def receive_video():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Initialize buffer for incoming data
    data = b""

    # Size of the packed frame length
    payload_size = struct.calcsize("Q")

    try:
        while True:
            # Receive frame size
            while len(data) < payload_size:
                # Receive data in chunks
                packet = client_socket.recv(4 * 1024)

                # Exit if no data received
                if not packet:
                    return
                
                data += packet
            
            # Unpack frame size
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            # Receive frame data based on the unpacked frame size
            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            
            # Deserialize frame data
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

            # Display the frame
            cv2.imshow("receiving...", frame)
            key = cv2.waitKey(10)

            # Close the socket
            if key == 13:
                break
    finally:
        client_socket.close()
        cv2.destroyAllWindows()


def main():
    receive_video()


if __name__ == "__main__":
    main()
