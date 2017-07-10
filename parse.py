# Vertigo 2016
import sys
import binascii
import struct

# First argument is the input binary file
try:
    logfile = sys.argv[1]
except IndexError:
    print "Usage: parse.py vtg_log.bin"
    exit(1)
metafile = logfile.split(".")[0] + ".meta.bin"
print "Using metafile %s" % metafile

# Try opening the meta file which we need for the FSRs
try:
    meta = open(metafile, "rb").read()
    accel_fsr = int(binascii.hexlify(meta[1] + meta[0]), 16)
    gyro_fsr = int(binascii.hexlify(meta[3] + meta[2]), 16)
    print "Accel/gyro FSRs are %d/%d" % (accel_fsr, gyro_fsr)
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

# The output file
outfile = logfile.split(".")[0] + ".csv"
csv = open(outfile, "w")

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
            csv.write("%d,%d,%f,%f,%f\n" % (p_ts, p_typ, gps_lon, gps_lat,
                gps_alt))
        elif p_typ == 2:
            ax = accel_fsr * float(struct.unpack(">h", packet[6] + packet[5])[0]) / 2**16
            ay = accel_fsr * float(struct.unpack(">h", packet[8] + packet[7])[0]) / 2**16
            az = accel_fsr * float(struct.unpack(">h", packet[10] + packet[9])[0]) / 2**16
            gx = gyro_fsr * float(struct.unpack(">h", packet[12] + packet[11])[0]) / 2**16
            gy = gyro_fsr * float(struct.unpack(">h", packet[14] + packet[13])[0]) / 2**16
            gz = gyro_fsr * float(struct.unpack(">h", packet[16] + packet[15])[0]) / 2**16
            csv.write("%d,%d,%f,%f,%f,%f,%f,%f\n" % (p_ts, p_typ, \
                    ax, ay, az, gx, gy, gz))
        elif p_typ == 3:
            q0 = struct.unpack(">f", packet[8] + packet[7] + packet[6] +
                    packet[5])[0]
            q1 = struct.unpack(">f", packet[12] + packet[11] + packet[10] +
                    packet[9])[0]
            q2 = struct.unpack(">f", packet[16] + packet[15] + packet[14] +
                    packet[13])[0]
            q3 = struct.unpack(">f", packet[20] + packet[19] + packet[18] +
                    packet[17])[0]
            csv.write("%d,%d,%f,%f,%f,%f\n" % (p_ts, p_typ, \
                    q0, q1, q2, q3))
        else:
            print "huh?"
        
        # Next log_msg_t
        i += 1
    except IndexError:
        print("Finished parsing %s - %d records" % (logfile, i))
        break

# We're done
csv.close()
