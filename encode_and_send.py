import sigmalib

tty_port = "/dev/ttyUSB0"

sigmalib.send_file("text.xml", tty_port)