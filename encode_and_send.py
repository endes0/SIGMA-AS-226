import sigmalib

tty_port = "/dev/ttyUSB0"

sigmalib.send_xml("text.xml", tty_port)