import RPi.GPIO as GPIO
import os
import time
from multiprocessing import Process

#initialize pins
powerPin = 6#3 #pin 5
ledPin = 14 #TXD
resetPin = 5#2 #pin 13
powerenPin = 26#4 #pin 5

#initialize GPIO settings
def init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(powerPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(resetPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.output(ledPin, GPIO.HIGH)
	GPIO.setup(powerenPin, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.output(powerenPin, GPIO.HIGH)
	GPIO.setwarnings(False)

#waits for user to hold button up to 1 second before issuing poweroff command
def poweroff():
	while True:
		#self.assertEqual(GPIO.input(powerPin), GPIO.LOW)
		#GPIO.wait_for_edge(powerPin, GPIO.FALLING)
		start = time.time()
		while GPIO.input(powerPin) == GPIO.HIGH:
			time.sleep(0.5)
		os.system("batocera-es-swissknife --emukill")
		os.system("shutdown -r now")

#blinks the LED to signal button being pushed
def ledBlink():
	while True:
		GPIO.output(ledPin, GPIO.HIGH)
		#self.assertEqual(GPIO.input(powerPin), GPIO.LOW)
		#GPIO.wait_for_edge(powerPin, GPIO.FALLING)
		start = time.time()
		while GPIO.input(powerPin) == GPIO.HIGH:
			time.sleep(0.5)
		while GPIO.input(powerPin) == GPIO.LOW:
			GPIO.output(ledPin, GPIO.LOW)
			time.sleep(0.2)
			GPIO.output(ledPin, GPIO.HIGH)
			time.sleep(0.2)

#resets the pi
def reset():
	time.sleep(60)
	while True:
		#self.assertEqual(GPIO.input(resetPin), GPIO.LOW)
		#GPIO.wait_for_edge(resetPin, GPIO.FALLING)
		start = time.time()
		count = 0
		while GPIO.input(resetPin) == GPIO.HIGH:
			count = 0
			time.sleep(0.5)
		while GPIO.input(resetPin) == GPIO.LOW and count < 4:
			count += 1
			time.sleep(0.5)
		if count != 0:
			os.system("batocera-es-swissknife --emukill")
			os.system("shutdown -r now")


if __name__ == "__main__":
	#initialize GPIO settings
	init()
	#create a multiprocessing.Process instance for each function to enable parallelism 
	powerProcess = Process(target = poweroff)
	powerProcess.start()
	ledProcess = Process(target = ledBlink)
	ledProcess.start()
	resetProcess = Process(target = reset)
	resetProcess.start()

	powerProcess.join()
	ledProcess.join()
	resetProcess.join()

	GPIO.cleanup()
