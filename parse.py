# Vertigo 2016
import sys
import binascii
import struct

# First argument
try:
    logfile = sys.argv[1]
except IndexError:
    print "Usage: parse.py vtg_log.bin"
    exit(1)
metafile = logfile.split(".")[0] + ".meta.bin"
print "Using metafile %s" % metafile

try:
    meta = open(metafile, "rb").read()
    accel_fsr = binascii.hexlify(meta[1] + meta[0])
    gyro_fsr = binascii.hexlify(meta[3] + meta[2])
    print "Accel/gyro FSRs are %d/%d" % (int(accel_fsr, 16), int(gyro_fsr, 16))
except IOError:
    print "Could not open meta file"

# size in bytes of a log_msg_t
MSG_LEN = 4 + 1 + 16

# Get raw
try:
    raw = open(logfile, "rb").read()
except IOError:
    print "Could not open binary log %s" % logfile
    exit(1)

# Run through
i = 0
while True:
    idx = MSG_LEN * i
    try:
        packet = raw[idx : idx + MSG_LEN]
        # Extract timestamp
        p_ts = int(binascii.hexlify(packet[3] + packet[2] + packet[1] +
            packet[0]), 16)
        # Extract message type
        p_typ = int(binascii.hexlify(packet[4]), 16)
        if p_typ == 1:
            # Extract GPS data
            gps_lon_b = packet[8] + packet[7] + packet[6] + packet[5]
            gps_lon = float(struct.unpack(">i", gps_lon_b)[0] / 1e7)
            gps_lat_b = packet[12] + packet[11] + packet[10] + packet[9]
            gps_lat = float(struct.unpack(">i", gps_lat_b)[0] / 1e7)
            gps_alt_b = packet[16] + packet[15] + packet[14] + packet[13]
            gps_alt = float(struct.unpack(">i", gps_alt_b)[0] / 1e3)
            print "Lon/lat/alt = %f/%f/%f" % (gps_lon, gps_lat, gps_alt)
        elif p_typ == 2:
            pass
        elif p_typ == 3:
            pass
        else:
            print "huh?"
        p_d0 = binascii.hexlify(packet[6] + packet[5])
        p_d1 = binascii.hexlify(packet[8] + packet[7])
        p_d2 = binascii.hexlify(packet[10] + packet[9])
        p_d3 = binascii.hexlify(packet[12] + packet[11])
        p_d4 = binascii.hexlify(packet[14] + packet[13])
        p_d5 = binascii.hexlify(packet[16] + packet[15])

        # Next log_msg_t
        i += 1
    except IndexError:
        print("Finished parsing %s" % logfile)
        break
