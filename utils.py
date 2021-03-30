'''
utility functions
'''

# constants
MAX_PAYLOAD = 1023

# Helper functions
def checksum(data):
    '''
    calculate the internet check sum: 16-bit
    '''
    s = 0

    if len(data) % 2 == 1:
        data = data + "\0"  # padding

        # loop taking 2 characters at a time
    for i in range(0, len(data), 2):
        w = ord(data[i]) + (ord(data[i + 1]) << 8)

        s = s + w

    s = (s >> 16) + (s & 0xffff)

    s = s + (s >> 16)

    # complement and mask to 4 byte short
    s = ~s & 0xffff

    return s


def not_corrupted(data, cs):
    return checksum(data) == cs
