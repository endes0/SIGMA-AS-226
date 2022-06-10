import sigmalib

tty_port = "/dev/ttyUSB0"

#send("This is a test, <BIG>TEST 1<OPEN>TEST 2<CLOSE>TEST 3<WAIT><9><JUMP>OK<CLEAR>")
#send("<DOFF>123456789ABCDEFG") # It can display 17 chars

# wait 9 aprox 3,3 sec
# wait 5 aprox 1,5 sec
#send("AAAAAA<WAIT><9>BBBBB<WAIT><5>CCCCC")

#open file(ignore newlines) and send
text = "".join(open("text.txt", "r").readlines())
sigmalib.send(text, tty_port)