import re
import sys


# Test length of command line args for server
def testArgLength():
    if len(sys.argv) != 2:
        print("Must use 1 command line arguments for server, Exiting!")
        sys.exit()


# Break port down to byte
def parsePort(port):
    out = re.findall(r'\d+', port)
    if len(out) != 1:
        print("Invalid port for input, Exiting!")
        sys.exit()
    else:
        if int(out[0]) > 65535:
            print("Invalid port for input: Port is larger than two byte range, Exiting!")
            sys.exit()
        elif int(out[0]) <= 1024:
            print("Invalid port for input: Port should be larger than 1024, Exiting!")
            sys.exit()
        else:
            out = int(out[0])
    return out


# Main method for server
if __name__ == '__main__':

    # Ensure correct number of command line arguments and extract
    testArgLength()
    portNum = str(sys.argv[1])

    portNum = parsePort(portNum)

    print(portNum)