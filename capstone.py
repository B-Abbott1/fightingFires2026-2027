
import csv
import time
import serial

PORT = "/dev/cu.usbserial-VNBRU2VU"
BAUD_RATE = 115200
DURATION = 10
OUTPUT_FILE = "vn100_data.csv"

# VNYMR field order from the VectorNav protocol
COLUMNS = [
    "timestamp_seconds",
    "yaw_deg", "pitch_deg", "roll_deg",
    "mag_x", "mag_y", "mag_z",
    "accel_x", "accel_y", "accel_z",
    "gyro_x", "gyro_y", "gyro_z",
]

rows_saved = 0
start_time = time.monotonic()

try:
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as sensor:
        print(f"Recording VN-100 data for {DURATION} seconds...")

        with open(OUTPUT_FILE, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(COLUMNS)

            while time.monotonic() - start_time < DURATION:
                raw_line = sensor.readline()

                if not raw_line:
                    continue

                try:
                    line = raw_line.decode("ascii").strip()
                except UnicodeDecodeError:
                    continue

                # Keep only complete VNYMR text messages
                if not line.startswith("$VNYMR,"):
                    continue

                # Remove checksum before parsing the numeric fields
                message = line.split("*", 1)[0]
                fields = message.split(",")

                # One message identifier plus 12 numeric values
                if len(fields) != 13:
                    continue

                try:
                    values = [float(value) for value in fields[1:]]
                except ValueError:
                    continue

                # Elapsed time since recording began
                timestamp = time.monotonic() - start_time

                writer.writerow([round(timestamp, 6)] + values)
                rows_saved += 1

        print(f"Recording finished.")
        print(f"Valid rows saved: {rows_saved}")
        print(f"CSV file: {OUTPUT_FILE}")

except serial.SerialException as error:
    print(f"Serial connection error: {error}")
