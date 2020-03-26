import re
import socket
import sys
import time


# Test length of command line args for client
def testArgLength():
    if len(sys.argv) != 6:
        print("Must use 5 command line arguments for client, Exiting!")
        sys.exit()


# Break port down to byte
def parsePort(port):
    out = re.findall(r'\d+', port)
    if len(out) != 1:
        print("Invalid port for input, Exiting!")
        sys.exit()
    else:
        if int(out[0]) > 65535:
            print("Invalid port for input: Port is larger than 65535 or 2 bytes, Exiting!")
            sys.exit()
        elif int(out[0]) <= 1024:
            print("Invalid port for input: Port should be larger than 1024, Exiting!")
            sys.exit()
        else:
            out = int(out[0])
    return out


# Main method for client
if __name__ == '__main__':

    # Set client mode (UDP/TCP)
    mode = "UDP"
    if (mode != "TCP") & (mode != "UDP"):
        print("Incorrect mode set. TCP and UDP are the only valid options. Exiting!")
        sys.exit()
    else:
        print("Running in " + mode + " mode")

    # Ensure correct number of command line arguments and extract data from them
    testArgLength()
    servName, portNum = str(sys.argv[1]), str(sys.argv[2])
    exeCount, timeDelay, command = int(sys.argv[3]), int(sys.argv[4]), str(sys.argv[5])

    # Build connection info tuple
    portNum = parsePort(portNum)
    ip = socket.gethostbyname(servName)
    sInfo = (str(ip), portNum)
    # sInfo = (socket.gethostname(), portNum)

    if mode == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(sInfo)
            print("Connection established")
            for a in range(0, exeCount):
                sock.send(bytes(command))
                response = sock.recv(1024)
                print("Received: " + str(response.decode()))
                time.sleep(timeDelay)
        except ConnectionError as e:
            sys.exit(e)
        finally:
            sock.close()

    if mode == "UDP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for a in range(0, exeCount):
            sock.sendto(bytes(command, 'utf-8'), sInfo)
            response, address = sock.recvfrom(1024)
            print("Received: " + str(response.decode()))
            time.sleep(timeDelay)
        sock.close()



