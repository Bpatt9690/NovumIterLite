import serial
import RPi.GPIO as GPIO
import time
import board
import adafruit_bno055
import adafruit_ltr390
from bmp280 import BMP280
import sys
import Adafruit_DHT



def DHTSetup():
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)

	if (humidity and temperature):
		return True
	else:
		return False


def ltr390Setup():
	i2c = board.I2C()
	ltr = adafruit_ltr390.LTR390(i2c)

	if ltr:
		return True
	else:
		return False


def bnoo55Setup():
	i2c = board.I2C()  # uses board.SCL and board.SDA
	sensor = adafruit_bno055.BNO055_I2C(i2c)
	last_val = 0xFFFF
	
	if sensor:
		return True
	else:
		return False


def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


def bme280Setup():
	try:
		from smbus2 import SMBus
	except ImportError:
		from smbus import SMBus

	# Initialise the BMP280
	bus = SMBus(1)
	bmp280 = BMP280(i2c_dev=bus)
	temperature = bmp280.get_temperature()
	pressure = bmp280.get_pressure()

	if (temperature and pressure):
		return True
	else:
		return False

def gpsSetup():
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
				return False

		except:
			pass



if __name__ == '__main__':

	sensorDict = {}

	sensorDict['dhStatus'] = DHTSetup()
	sensorDict['gpsStatus'] = gpsSetup()
	sensorDict['bme280Status'] = bme280Setup()
	sensorDict['bnoo55Status'] = bnoo55Setup()
	sensorDict['ltr390Status'] = ltr390Setup()

	if all(value == True for value in sensorDict.values()):
		print('All Systems Go')

	else:
		for k, v in sensorDict.items():
			if v == False:
				print(k,v)

	print(sensorDict)