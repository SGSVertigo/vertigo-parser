# Vertigo 2016
import binascii
import struct

logfile = "vertigo.bin"

# size in bytes of a log_msg_t
MSG_LEN = 4 + 1 + 6*2

# Get raw
raw = open(logfile, "rb").read()

# Run through
i = 0
while True:
    idx = MSG_LEN * i
    try:
        packet = raw[idx : idx + MSG_LEN]
        p_ts = binascii.hexlify(packet[3] + packet[2] + packet[1] + packet[0])
        p_typ = binascii.hexlify(packet[4])
        p_d0 = binascii.hexlify(packet[6] + packet[5])
        p_d1 = binascii.hexlify(packet[8] + packet[7])
        p_d2 = binascii.hexlify(packet[10] + packet[9])
        p_d3 = binascii.hexlify(packet[12] + packet[11])
        p_d4 = binascii.hexlify(packet[14] + packet[13])
        p_d5 = binascii.hexlify(packet[16] + packet[15])
        print "%dms | %02d | %04X,%04X,%04X,%04X,%04X,%04X" % (int(p_ts, 16), int(p_typ, 16),
                int(p_d0, 16),
                int(p_d1, 16),
                int(p_d2, 16),
                int(p_d3, 16),
                int(p_d4, 16),
                int(p_d5, 16))
        i += 1
    except IndexError:
        print("Finished parsing %s" % logfile)
        break
