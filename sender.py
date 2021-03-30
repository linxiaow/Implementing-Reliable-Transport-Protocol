import json
from socket import socket, AF_INET, SOCK_DGRAM, error as socket_error
import argparse
import sys

class Sender:
    # TODO: Place States

    # Initiate Receiver
    # (host, port) will be used to create UDP Server Socket
    # The server socket will be receiving information from new_udpl that
    # is reading from sender_skeleton.py
    # (dest_host, dest_port) will create a client socket
    # to connect ACK/NAK to receive.py
    # Initialize your state/variables
    def __init__(self, args):
        # How to access the variables within args...
        self.host = args.host
        self.port = args.port
        self.dest_host = args.dest_host
        self.dest_port = args.dest_port
        self.socket = None
        # raise NotImplementedError

    # Run a while loop that will change status depending on FIN, etc.
    def start(self):
        try:
            self.socket = socket(AF_INET, SOCK_DGRAM)
        except socket_error:
            print('Failed to create client socket')
            sys.exit()
        while True:
            msg = input('Enter message to send : ')
            try:
                # Set the whole string
                self.socket.sendto(msg.encode(), (self.dest_host, self.dest_port))

                # receive data from client (data, addr)
                reply, addr = self.socket.recvfrom(1024)
                print('Server reply : ' + reply.decode())

            except socket_error as msg:
                print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
                sys.exit()
        # raise NotImplementedError

    # Read inbound packet from udpl that is connected to receiver
    def inbound(self):
        raise NotImplementedError

    # setup output state
    # read input from stdin for payload data
    def outbound(self):
        raise NotImplementedError

    # Call this function when it is time to send a FIN to receive.py
    def end(self):
        raise NotImplementedError

    # Call this function if there is a timeout
    def timer_interrupt(self):
        raise NotImplementedError

    # Call this function to create packet
    def make_packet(self, line, is_fin=False):
        raise NotImplementedError

    # send the packet to receive.py
    def send_outbound(self):
        raise NotImplementedError

    # TODO: Create the checksum of your UDP packet
    def get_checksum(self, packet):
        raise NotImplementedError


# Main method to read command line arguments
def main():
    parser = argparse.ArgumentParser()
    # To create server socket that will GET data from receive.py
    parser.add_argument('--host', dest='host', action='store', required=True,
                        help='Listen to this host, which has new_udpl instances reading '
                             'from receiver_refactor.py', type=str)
    parser.add_argument('--port', dest='port', action='store', required=True,
                        help='Listen to this port, which is the port of udpl_instance reading '
                             'from receiver_refactor.py', type=int)
    # To create client socket to SEND data to receive.py
    parser.add_argument('--dest_host', dest='dest_host', action='store', required=True,
                        help='Destination Host to new_udpl instance which sends to sender_skeleton.py', type=str)
    parser.add_argument('--dest_port', dest='dest_port', action='store', required=True,
                        help='Destination Port to new_udpl instance which sends to sender_skeleton.py', type=int)
    # To set timeout parameter on runtime for UDP sockets
    # Would recommend using 1-2 second timeout
    parser.add_argument('--timeout', dest='timeout', action='store', required=True,
                        help='set timeout for sender client socket', type=int)
    args = parser.parse_args()

    print(args)
    # Create sender object and send data
    sender = Sender(args)
    sender.start()


if __name__ == "__main__":
    main()
