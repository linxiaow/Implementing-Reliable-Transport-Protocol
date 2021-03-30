import json
from socket import socket, AF_INET, SOCK_DGRAM, error as socket_error
import argparse
import sys


class Receiver:
    # TODO: Place States

    # Initiate Receiver
    # (host, port) will be used to create UDP Server Socket
    # The server socket will be receiving information from new_udpl that
    # is reading from sender_skeleton.py
    # (dest_host, dest_port) will create a client socket
    # to connect ACK/NAK to sender_skeleton.py
    # Initialize your state/variables
    def __init__(self, args):
        # How to access the variables within args...
        self.host = args.host
        self.port = args.port
        self.dest_host = args.dest_host
        self.dest_port = args.dest_port
        self.socket = None
        # raise NotImplementedError

    # Run a while loop that will change status depending on FIN flag
    def start(self):
        try:
            self.socket = socket(AF_INET, SOCK_DGRAM)
        except socket_error as msg:
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        try:
            self.socket.bind((self.host, self.port))
        except socket_error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        print("Server socket created and bind to host {} and port {}!".format(self.host, self.port))

        try:
            while True:
                print("---------------------------------------------------")
                data, addr = self.socket.recvfrom(2048)
                reply_data = json.loads(data.decode('utf-8', 'ignore'))

                self.socket.sendto(reply_data["data"].encode(), addr)
                print("**Server Message sent**:", reply_data)
            # raise NotImplementedError
        except KeyboardInterrupt:
            self.socket.close()
            sys.exit()

    # Create your outbound packet to send to sender_skeleton.py
    # Refer to this:
    # https://www.binarytides.com/programming-udp-sockets-in-python/
    def outbound(self, acknum):
        raise NotImplementedError

    # TODO: This method is called when receive.py gets a packet from sender_skeleton.py
    # Check for the following
    # 1- Is the checksum correct?
    # 2- Check sequence number/ACK number
    # 3- Check if sender_skeleton.py wants to terminate
    # Refer to this:
    # https://www.binarytides.com/programming-udp-sockets-in-python/
    def inbound(self):
        raise NotImplementedError

    # TODO: Create the checksum of your UDP packet
    def get_checksum(self, packet):
        raise NotImplementedError


# Main method to read command line arguments
def main():
    parser = argparse.ArgumentParser()
    # To create server socket that will GET data from sender_skeleton.py
    parser.add_argument('--host', dest='host', action='store', required=True,
                        help='Listen to this host, which has new_udpl instances reading '
                             'from sender_skeleton.py', type=str)
    parser.add_argument('--port', dest='port', action='store', required=True,
                        help='Listen to this port, which is the port of udpl_instance reading '
                             'from sender_skeleton.py', type=int)
    # To create client socket to SEND data to sender_skeleton.py
    parser.add_argument('--dest_host', dest='dest_host', action='store', required=True,
                        help='Destination Host to new_udpl instance which sends to sender_skeleton.py', type=str)
    parser.add_argument('--dest_port', dest='dest_port', action='store', required=True,
                        help='Destination Port to new_udpl instance which sends to sender_skeleton.py', type=int)
    args = parser.parse_args()

    print(args)
    # Create Receiver and start listening
    receiver = Receiver(args)
    receiver.start()


if __name__ == "__main__":
    main()
