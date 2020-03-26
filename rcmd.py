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
    mode = input("Enter 'TCP' or 'UDP' to set client mode: ")
    if (mode.upper() != "TCP") & (mode.upper() != "UDP"):
        print("Incorrect mode set. TCP and UDP are the only valid options. Exiting!")
        sys.exit()
    else:
        print("Client running in " + mode.upper() + " mode\n")

    # Ensure correct number of command line arguments and extract data from them
    testArgLength()
    servName, portNum = str(sys.argv[1]), str(sys.argv[2])
    exeCount, timeDelay, command = int(sys.argv[3]), int(sys.argv[4]), str(sys.argv[5])

    # Build connection info tuple
    portNum = parsePort(portNum)
    ip = socket.gethostbyname(servName)
    sInfo = (str(ip), portNum)
    # sInfo = (socket.gethostname(), portNum)

    # Connect to server using TCP or send messages using UDP
    if mode.upper() == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(sInfo)
            print("Connection established")
            for a in range(0, exeCount):
                sock.send(bytes(command, 'utf-8'))
                response = sock.recv(1024)
                print("Received: " + str(response.decode()))
                if a != exeCount - 1:
                    time.sleep(timeDelay)
        except ConnectionError as e:
            sys.exit(e)
        finally:
            print("Connection closed")
            sock.close()

    if mode.upper() == "UDP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for a in range(0, exeCount):
            sock.sendto(bytes(command, 'utf-8'), sInfo)
            response, address = sock.recvfrom(1024)
            print("Received: " + str(response.decode()))
            if a != exeCount - 1:
                time.sleep(timeDelay)
        sock.close()



