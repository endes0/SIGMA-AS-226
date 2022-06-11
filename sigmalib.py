from click import echo
import serial  # pyserial
import unidecode


START = b'\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xBB\x8C'
END = b'\x80'
CMD_DICT = {
    "CLEAR": 0x8C,
    "LEFT": 0x81,
    "RIGHT": 0x82,
    "UP": 0x83,
    "DOWN": 0x84,
    "JUMP": 0x85,
    "OPEN": 0x86,
    "CLOSE": 0x87,
    "FLASH": 0x88,
    "FLASH_SCROLL": 0x89,
    "DOFF": 0x8A,
    "BIG": 0x8B,
    "RANDOM": 0x8E,
    "CLOCK": 0x11,

    "WAIT": 0x8F,
    "SPEED": 0x8D
}


def cmd_to_byte(cmd):
    if cmd >= '1' and cmd <= '9':
        return (ord(cmd) - ord('0') + 0x30).to_bytes(1, 'big')
    elif cmd in CMD_DICT:
        return CMD_DICT[cmd].to_bytes(1, 'big')
    else:
        return b'0'


def encode(line):
    # state machine for encoding
    cmd = ""
    is_cmd_reading = False
    final = bytearray()
    is_escape = False
    counter = 0
    for c in line:
        if c == '<' and not is_escape:
            is_cmd_reading = True
            cmd = ""
        elif c == '>' and is_cmd_reading:
            if counter > 0 and counter < 16 and cmd != "SPEED" and cmd != "WAIT" and not cmd.isnumeric():
                # center adding spaces
                #final.extend(':'.encode('ascii') * ((16 - counter)//2))
                counter = 0
            elif cmd != "SPEED" and cmd != "WAIT" and not cmd.isnumeric():
                counter = 0

            is_cmd_reading = False
            final += cmd_to_byte(cmd)
        elif c == '\\' and not is_escape:
            is_escape = True
        elif is_cmd_reading:
            cmd += c
        else:
            if is_escape:
                is_escape = False
                final += '\\'.encode('ascii')
                counter += 1
            
            if c == '\n':
              pass
            elif c == '\r':
              pass
            elif c == '\t':
              pass
             # yeah, It's strange, but there are a lot of symbols coded not in ascii
             #TODO: a dict like CMD_DICT
            elif c == ' ':
                final += ':'.encode('ascii')
                counter += 1
            elif c == ':':
                final += ' '.encode('ascii')
                counter += 1
            elif c == '<':
                final += '_'.encode('ascii')
                counter += 1
            elif c == '[':
                final += b'\x0E'
                counter += 1
            elif c == ']':
                final += b'\x1E'
                counter += 1
            else:
                final += unidecode.unidecode(c).encode('ascii')
                counter += 1
    return final


def send(line, tty_port):
    port = serial.Serial(tty_port, 2400, timeout=1)
    line = encode(line)
    print(line)
    line = START + line + END
    port.write(line)
    port.close()

def fuzz(tty_port):
    port = serial.Serial(tty_port, 2400, timeout=1)
    line = START
    line += encode("<BIG>")

    for i in range(0, 18):
        line += encode(str(i))
        line += encode("<WAIT><1>")
        line += i.to_bytes(1, 'big')
        line += encode("    ")

    line += END
    print(line)
    port.write(line)
    port.close()