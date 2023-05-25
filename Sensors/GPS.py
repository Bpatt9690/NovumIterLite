import serial
import RPi.GPIO as GPIO
import time


def gpsTest():
	gps_dict = {}

	gps = serial.Serial(
		"/dev/ttyUSB0",
		timeout=None,
		baudrate=4800,
		xonxoff=False,
		rtscts=False,
		dsrdtr=False,
	)

	while True:
		line = gps.readline()
		time.sleep(1)

		try:
			line = line.decode("utf-8")
			sline = line.split(",")

			if sline[0] == "$GPGGA":
				gps_dict["Time UTC"] = sline[1]
				gps_dict["Lattitude"] = float(sline[2]) / 100
				gps_dict["Lattitude Direction"] = sline[3]
				gps_dict["Longitude"] = float(sline[4]) / 100
				gps_dict["Longitude Direction"] = sline[5]
				gps_dict["Number Satellites"] = sline[7]
				gps_dict["Alt Above Sea Level"] = sline[9]
				print("GPS Sensor Data Retrieval Successful \n {}".format(gps_dict))
				return True

		except:
			print('GPS Sensor Data Retrieval Failure')



if __name__ == '__main__':
	gpsTest()