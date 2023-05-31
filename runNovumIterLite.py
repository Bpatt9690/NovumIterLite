import os
from setupRover import setup
from Data.aggregateData import data
from Data.transmitData import transmit
import time

def main():

	setupNovumIterLite = setup()
	setupNovumIterLite.systemStatus()
	dataAgg = data()
	dataTransmit = transmit()

	while(1):
		dataAgg.dataAggregate()
		dataTransmit.dataTransmission()
		time.sleep(5*60)

if __name__ == '__main__':
	main()
