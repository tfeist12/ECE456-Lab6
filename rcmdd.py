import datetime
import os
import re
import socket
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


# Modify read command if necessary
def modCom(commandOut):
    if len(commandOut) == 0:
        commandOut = "No Command Output"
    if commandOut[len(commandOut) - 1] == '\n':
        commandOut = commandOut[:-1]
    return commandOut


# Main method for server
if __name__ == '__main__':

    # Set server mode (UDP/TCP)
    mode = input("Enter 'TCP' or 'UDP' to set server mode: ")
    if (mode.upper() != "TCP") & (mode.upper() != "UDP"):
        print("Incorrect mode set. TCP and UDP are the only valid options. Exiting!")
        sys.exit()
    else:
        print("Server running in " + mode.upper() + " mode")

    # Ensure correct number of command line arguments and extract
    testArgLength()
    portNum = str(sys.argv[1])

    # Build connection info tuple
    portNum = parsePort(portNum)
    sInfo = ("0.0.0.0", portNum)

    if mode.upper() == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(sInfo)
        sock.listen(5)

        while True:
            connection, address = sock.accept()
            print("\nStatus: Connected to " + address[0])
            count = 0

            while True:
                command = connection.recv(1024)
                if len(command) != 0:
                    cOut = os.popen(command.decode()).read()
                    cOut = modCom(cOut)
                    # Make command appear below info if necessary
                    lineAdd = ""
                    if '\n' in cOut:
                        lineAdd = "Command Output Below:\n"
                    outString = str(count + 1) + " - " + str(datetime.datetime.now().time())[:8] + " - " + lineAdd + cOut
                    print("Command \'" + command.decode() + "\' from " + address[0] + "\n" + outString)
                    connection.send(bytes(outString, 'utf-8'))
                    count += 1
                else:
                    print("Status: Client closed connection")
                    connection.close()
                    break

    if mode.upper() == "UDP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(sInfo)
        count = 0

        print("")
        while True:
            command, address = sock.recvfrom(1024)
            cOut = os.popen(command.decode()).read()
            cOut = modCom(cOut)
            # Make command appear below info if necessary
            lineAdd = ""
            if '\n' in cOut:
                lineAdd = "Command Output Below:\n"
            outString = str(count + 1) + " - " + str(datetime.datetime.now().time())[:8] + " - " + lineAdd + cOut
            print("Command \'" + command.decode() + "\' from " + address[0] + "\n" + outString)
            sock.sendto(bytes(outString, 'utf-8'), address)
            count += 1
