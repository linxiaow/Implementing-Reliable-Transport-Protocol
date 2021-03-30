import json
from socket import socket, AF_INET, SOCK_DGRAM, error as socket_error, timeout
import argparse
import sys
from utils import MAX_PAYLOAD
from utils import checksum, not_corrupted


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
        self.timeout = args.timeout
        self.seq = 0  # begin with 0
        self.buffer = []

    # Run a while loop that will change status depending on FIN, etc.
    def start(self):
        try:
            self.socket = socket(AF_INET, SOCK_DGRAM)
        except socket_error:
            print('Failed to create client socket')
            sys.exit()
        try:
            self.socket.bind((self.host, self.port))
        except socket_error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        try:
            inf = sys.stdin
            debug_index = 0
            current_payload = inf.read(MAX_PAYLOAD)

            # loop until you everything is read
            while len(current_payload) > 0:

                # FIN
                is_fin = False
                if len(current_payload) < MAX_PAYLOAD:
                    is_fin = True
                # else:
                self.buffer.append(self.make_packet(current_payload, self.seq, is_fin=is_fin, index=debug_index))
                current_payload = inf.read(MAX_PAYLOAD)
                self.seq = 1 - self.seq
                debug_index += 1

            self.seq = 0
            index = 0
            while index < len(self.buffer):
                try:
                    while True:
                        print("[INFO]: Transmitting No.{} packet...".format(index))
                        is_send = self.outbound(self.buffer[index])
                        if is_send:
                            break
                    self.socket.settimeout(self.timeout)

                    # receive data from client (data, addr)
                    while True:
                        is_received = self.inbound()
                        if is_received:
                            self.seq = 1 - self.seq  # alternating bit
                            break
                    # print('Server reply : ' + reply.decode())
                except timeout:
                    print("Timeout occurs! retransmit......")
                    self.socket.settimeout(None)
                    continue
                except socket_error as msg:
                    print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
                    sys.exit()
                index += 1
        except KeyboardInterrupt:
            self.socket.close()
            sys.exit()

        # raise NotImplementedError

    # Read inbound packet from udpl that is connected to receiver
    def inbound(self):
        payload, addr = self.socket.recvfrom(2048)
        print("sender received ACK!")
        if not_corrupted(payload, is_from_sender=False):
            load_json = json.loads(payload)  # guarantee to be decodable
            ack = load_json["acknowledgement_number"]
            if ack == self.seq:
                return True
            else:
                print("*** ack not equal to seq! ***")
                return False
        else:
            print("*** data corrupted! ***")
            return False
        # raise NotImplementedError

    # setup output state
    # read input from stdin for payload data
    def outbound(self, pkt):
        sndpket = pkt
        self.socket.sendto(sndpket.encode(),
                           (self.dest_host, self.dest_port))
        return True
        # raise NotImplementedError

    # Call this function when it is time to send a FIN to receive.py
    def end(self):
        raise NotImplementedError

    # Call this function if there is a timeout
    def timer_interrupt(self):
        raise NotImplementedError

    # Call this function to create packet
    def make_packet(self, data, seq, is_fin=False, index=0):
        # index is only for debugging usage to see the order of packet
        # transfer in json format
        packet = {
            "FIN": int(is_fin),
            "sequence_number": seq,
            "data": data,
            "internet_checksum": self.get_checksum(data),
            "index": index
        }

        packet = json.dumps(packet)
        return packet
        # raise NotImplementedError

    # send the packet to receive.py
    def send_outbound(self):
        raise NotImplementedError

    # TODO: Create the checksum of your UDP packet
    def get_checksum(self, packet):
        internet_checksum = checksum(packet)
        return internet_checksum


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

    # Create sender object and send data
    sender = Sender(args)
    sender.start()


if __name__ == "__main__":
    main()
