import serial
import RPi.GPIO as GPIO
import time
import board
import adafruit_bno055
import adafruit_ltr390
from bmp280 import BMP280


def ltr390Test():
	i2c = board.I2C()
	ltr = adafruit_ltr390.LTR390(i2c)
	print("UV:", ltr.uvs, "\t\tAmbient Light:", ltr.light)
	print("UV Index:", ltr.uvi, "\t\tLux:", ltr.lux)

def bnoo55Test():
	i2c = board.I2C()  # uses board.SCL and board.SDA
	# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
	sensor = adafruit_bno055.BNO055_I2C(i2c)

	# If you are going to use UART uncomment these lines
	# uart = board.UART()
	# sensor = adafruit_bno055.BNO055_UART(uart)

	last_val = 0xFFFF
	print("Temperature: {} degrees C".format(sensor.temperature))
	print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
	print("Magnetometer (microteslas): {}".format(sensor.magnetic))
	print("Gyroscope (rad/sec): {}".format(sensor.gyro))
	print("Euler angle: {}".format(sensor.euler))
	print("Quaternion: {}".format(sensor.quaternion))
	print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
	print("Gravity (m/s^2): {}".format(sensor.gravity))
	print()

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


def bme280Test():
	try:
		from smbus2 import SMBus
	except ImportError:
		from smbus import SMBus

	# Initialise the BMP280
	bus = SMBus(1)
	bmp280 = BMP280(i2c_dev=bus)
	temperature = bmp280.get_temperature()
	pressure = bmp280.get_pressure()
	print('Temperature: {:05.2f}*C Pressure: {:05.2f}hPa\n'.format(temperature, pressure))

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
				print("\nGPS Sensor Data Retrieval Successful\n {}".format(gps_dict))
				return True

		except:
			pass



if __name__ == '__main__':
	while(1):
		gpsTest()
		print("\n-------------------------------------------------------------------------\n")
		bme280Test()
		print("\n-------------------------------------------------------------------------\n")
		bnoo55Test()
		print("\n-------------------------------------------------------------------------\n")
		ltr390Test()
		print("\n-------------------------------------------------------------------------\n")
		print()
		time.sleep(5)