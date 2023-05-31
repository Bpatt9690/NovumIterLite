import serial
import RPi.GPIO as GPIO
import time
import board
import adafruit_bno055
import adafruit_ltr390
from bmp280 import BMP280
import sys
import Adafruit_DHT
import threading
import subprocess


class data:

	def __init__(self):
		pass

	def onboardCamera(self):
		# Command to execute
		command = "libcamera-jpeg -t 5000 -o test.jpg"
		subprocess.Popen(command, shell=True)
		time.sleep(20)
		#Remove file after sending

	def cameraThread(self):
		# Create a thread to run the command
	    thread = threading.Thread(target=self.onboardCamera)
	    thread.start()

	    # Wait for the thread to finish
	    thread.join()

	def DHTData(self):
		humidity, temperature = Adafruit_DHT.read_retry(11, 4)
		#print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
		return humidity, temperature

	def ltr390Data(self):
		i2c = board.I2C()
		ltr = adafruit_ltr390.LTR390(i2c)
		return ltr.uvs, ltr.light, ltr.uvi, ltr.lux

	def bnoo55Data(self):
		i2c = board.I2C()  # uses board.SCL and board.SDA
		sensor = adafruit_bno055.BNO055_I2C(i2c)
		last_val = 0xFFFF
		return sensor.temperature, sensor.acceleration, sensor.magnetic, sensor.gyro, sensor.linear_acceleration, sensor.gravity

	def temperature(self):
	    global last_val
	    result = sensor.temperature
	    if abs(result - last_val) == 128:
	        result = sensor.temperature
	        if abs(result - last_val) == 128:
	            return 0b00111111 & result
	    last_val = result
	    return result


	def bme280Data(self):
		try:
			from smbus2 import SMBus
		except ImportError:
			from smbus import SMBus

		bus = SMBus(1)
		bmp280 = BMP280(i2c_dev=bus)
		temperature = bmp280.get_temperature()
		pressure = bmp280.get_pressure()
		return temperature, pressure

	def gpsData(self):
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
					return gps_dict

			except:
				pass



	def dataAggregate(self):

		dataDict = {}
		dhtHumitidy,dhtTemperature = self.DHTData()
		uvs,light,uvi,lux = self.ltr390Data()
		temperature,acceleration,magnetic,gyro,linear_acceleration,gravity = self.bnoo55Data()
		bmeTemp, pressure = self.bme280Data()
		gps_dict = self.gpsData()

		dataDict['DHT Humidity'] = dhtHumitidy
		dataDict['DHT Temperature'] = dhtTemperature
		dataDict['UVS'] = uvs
		dataDict['Light'] = light
		dataDict['Uvi'] = uvi
		dataDict['Lux'] = lux
		dataDict['BNO055 Temperature'] = temperature
		dataDict['Acceleration'] = acceleration
		dataDict['Magnetic'] = magnetic
		dataDict['Gyro'] = gyro
		dataDict['BME280 Temp'] = temperature
		dataDict['Pressure'] = pressure
		dataDict['GPS Data'] = gps_dict
		print(dataDict)
		time.sleep(5)
		self.cameraThread()



