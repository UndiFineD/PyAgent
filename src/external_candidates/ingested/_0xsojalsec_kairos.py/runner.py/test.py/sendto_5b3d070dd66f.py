# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Kairos\Runner\test\sendto.py
import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a message
sock.sendto(b"Hello, World!", ("localhost", 12345))
