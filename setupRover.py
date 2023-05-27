import serial
import RPi.GPIO as GPIO
import time
import board
import adafruit_bno055
import adafruit_ltr390
from bmp280 import BMP280
import sys
import Adafruit_DHT
from dotenv import load_dotenv
from Logging.fileLogging import logger
import os

class setup:

	def __init__(self):
		pass

	def logData(self,data):
		load_dotenv()
		level = os.getenv("LOGGING_LEVEL")
		logs = logger()
		logs.logData(data,level)

	def systemStatus(self):
		sensorDict = {}
		sensorDict['dhStatus'] = self.DHTSetup()
		sensorDict['gpsStatus'] = self.gpsSetup()
		sensorDict['bme280Status'] = self.bme280Setup()
		sensorDict['bnoo55Status'] = self.bnoo55Setup()
		sensorDict['ltr390Status'] = self.ltr390Setup()

		if all(value == True for value in sensorDict.values()):
			self.logData('All Systems Go')
			print()
			print('\tAll Systems Go\n')
			print()

		else:
			for k, v in sensorDict.items():
				if v == False:
					self.logData("Systems Failure")

	def DHTSetup(self):
		humidity, temperature = Adafruit_DHT.read_retry(11, 4)

		if (humidity and temperature):
			return True
		else:
			return False

	def ltr390Setup(self):
		i2c = board.I2C()
		ltr = adafruit_ltr390.LTR390(i2c)

		if ltr:
			return True
		else:
			return False

	def bnoo55Setup(self):
		i2c = board.I2C()  # uses board.SCL and board.SDA
		sensor = adafruit_bno055.BNO055_I2C(i2c)
		last_val = 0xFFFF
		
		if sensor:
			return True
		else:
			return False

	def temperature(self):
	    global last_val  # pylint: disable=global-statement
	    result = sensor.temperature
	    if abs(result - last_val) == 128:
	        result = sensor.temperature
	        if abs(result - last_val) == 128:
	            return 0b00111111 & result
	    last_val = result
	    return result

	def bme280Setup(self):
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

	def gpsSetup(self):
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
					return True

			except:
				pass

