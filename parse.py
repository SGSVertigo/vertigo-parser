# Vertigo 2016
import sys
import binascii
import struct

# First argument is the input binary file
try:
    logfile = sys.argv[1]
except IndexError:
    print("Usage: parse.py vtg_log.bin")
    exit(1)
metafile = logfile.split(".")[0] + ".meta.bin"
print("Using metafile %s" % metafile)

# Try opening the meta file which we need for the FSRs
try:
    meta = open(metafile, "rb").read()
    accel_fsr = int.from_bytes(meta[0:2], byteorder='little')
    gyro_fsr = int.from_bytes(meta[2:4], byteorder='little')
    print("Accel/gyro FSRs are %d/%d" % (accel_fsr, gyro_fsr))
except IOError:
    print("Could not open meta file")

# size in bytes of a log_msg_t
MSG_LEN = 4 + 1 + 16

# Get raw
try:
    raw = open(logfile, "rb").read()
except IOError:
    print("Could not open binary log %s" % logfile)
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
        p_ts = int.from_bytes(packet[0:4], byteorder='little')
        # Extract message type
        p_typ = packet[4]
        if p_typ == 1:
            # Extract GPS data
            gps_lon = struct.unpack("<i", packet[5:9])[0] / 1e7
            gps_lat = struct.unpack("<i", packet[9:13])[0] / 1e7
            gps_alt = struct.unpack("<i", packet[13:17])[0] / 1e3
            csv.write("%d,%d,%f,%f,%f\n" % (p_ts, p_typ, gps_lon, gps_lat,
                gps_alt))
        elif p_typ == 2:
            ax = accel_fsr * struct.unpack("<h", packet[5:7])[0] / 2**16
            ay = accel_fsr * struct.unpack("<h", packet[7:9])[0] / 2**16
            az = accel_fsr * struct.unpack("<h", packet[9:11])[0] / 2**16
            gx = gyro_fsr * struct.unpack("<h", packet[11:13])[0] / 2**16
            gy = gyro_fsr * struct.unpack("<h", packet[13:15])[0] / 2**16
            gz = gyro_fsr * struct.unpack("<h", packet[15:17])[0] / 2**16
            csv.write("%d,%d,%f,%f,%f,%f,%f,%f\n" % (p_ts, p_typ, \
                    ax, ay, az, gx, gy, gz))
        elif p_typ == 3:
            q0 = struct.unpack("<f", packet[5:9])[0]
            q1 = struct.unpack("<f", packet[9:13])[0]
            q2 = struct.unpack("<f", packet[13:17])[0]
            q3 = struct.unpack("<f", packet[17:21])[0]
            csv.write("%d,%d,%f,%f,%f,%f\n" % (p_ts, p_typ, \
                    q0, q1, q2, q3))
        else:
            print("huh?")
        
        # Next log_msg_t
        i += 1
    except IndexError:
        print(("Finished parsing %s - %d records" % (logfile, i)))
        break

# We're done
csv.close()
