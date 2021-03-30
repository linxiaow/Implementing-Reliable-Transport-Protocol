"""
utility functions
"""

import json

# constants
MAX_PAYLOAD = 1024

# Helper functions
def checksum(data):
    """
    calculate the internet check sum: 16-bit
    """
    data = str(data)
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


def not_corrupted(payload, is_from_sender):
    try:
        json_data = json.loads(payload)
        if is_from_sender:
            data = json_data["data"]
            index = json_data["index"]
            FIN = json_data["FIN"]
        else:
            # receiver use ack_number instead of data
            data = json_data["acknowledgement_number"]
        cs = json_data["internet_checksum"]
    except json.decoder.JSONDecodeError:
        print("**[WARNING]**: payload itself is corrupted...")
        return False
    except KeyError as e:
        print("**[WARNING]**: keyError occurs and json is corrupted: ", str(e))
        return False
    except Exception as e:
        print("**[WARNING]**: Unknown Error: ", str(e))
        return False

    if checksum(data) == cs:
        return True
    else:
        print("**[WARNING]**: checksum does not match data, the data is corrupted...")
        return False
