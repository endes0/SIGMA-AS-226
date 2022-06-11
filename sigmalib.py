import serial  # pyserial
import unidecode
from defusedxml.ElementTree import fromstring, parse


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
# yeah, it's strange, but there are a lot of symbols not coded in ascii
ENCODING_DICT = {
    " ": ":".encode('ascii'),
    ":": " ".encode('ascii'),
    "<": "_".encode('ascii'),
    "_": "<".encode('ascii'),
    "[": b'\x0E',
    "]": b'\x1E'
}


def encode_cmd_number(num):
    return (ord(num) - ord('0') + 0x30).to_bytes(1, 'big')


def process_text(text, align=True):
    # encode text
    text = unidecode.unidecode(text)
    for key in ENCODING_DICT:
        text = text.replace(key, ENCODING_DICT[key])

    # center align text if it is not too long and not has noalign attribute
    if align:
        if len(text) <= 16:
            text = text.center(16, ':')

    return text


def xml_encode(xml_root):
    final = bytearray()
    for anim in xml_root:
        # encode command depending on the type of tag
        if anim.tag.upper() in CMD_DICT:
            final += CMD_DICT[anim.tag.upper()].to_bytes(1, 'big')
        else:
            # throw error
            pass

        # Special cases
        if anim.tag == "wait":
            if "time" in anim.attrib:
                final += encode_cmd_number(anim.atrib["time"])
        elif anim.tag == "speed":
            if "time" in anim.attrib:
                final += encode_cmd_number(anim.atrib["time"])
        elif anim.tag == "clock":
            pass
        else:
            align = "noalign" not in anim.attrib

            final += process_text(anim.text, align).encode('ascii')
            for child in anim:
                final += xml_encode(child)

    return final


def encode(line):
    return xml_encode(fromstring(line))


def send_encoded(data, tty_port):
    port = serial.Serial(tty_port, 2400, timeout=1)
    print(data)
    data = START + data + END
    port.write(data)
    port.close()


def send_line(line, tty_port):
    send_encoded(encode(line), tty_port)


def send_file(xml_file, tty_port):
    send_encoded(xml_encode(parse(xml_file).getroot()), tty_port)


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
