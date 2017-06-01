#!/usr/bin/env python3
# Copyright(c) 2017 by craftyguy "Clayton Craft" <clayton@craftyguy.net>
# Distributed under GPLv3+ (see COPYING) WITHOUT ANY WARRANTY.

import argparse
import hashlib
import socket

# Buffer used for reading application & calculating its checksum
BUF_SIZE = 1024

def main():
    """Send a Micropython application to an ESP8266"""

    parser = argparse.ArgumentParser(description='Send update to ESP8266 running MicroPython')
    parser.add_argument('-i', '--ip', action='store', required=True, help='IP address of the ESP8266')
    parser.add_argument('-p', '--port', action='store', required=True, help='Port to connect to', type=int)
    parser.add_argument('app', action='store', help='MicroPython application to send (e.g. app.py)')

    args = parser.parse_args()

    s = socket.socket()
    s.connect((args.ip, args.port))

    # Calculate sha256 checksum for file
    hashr = hashlib.sha256()
    with open(args.app, 'rb') as f:
        buf = f.read(BUF_SIZE)
        while len(buf) > 0:
            hashr.update(buf)
            buf = f.read(BUF_SIZE)
    checksum = hashr.digest()
    s.send(checksum)

    # Send file to esp8266
    with open(args.app, 'rb') as f:
        buf = f.read(BUF_SIZE)
        while len(buf) > 0:
            s.send(buf)
            buf = f.read(BUF_SIZE)
    s.close


if __name__ == "__main__":
    main()
