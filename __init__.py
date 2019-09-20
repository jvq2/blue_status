import logging
import time
import sys

import bluetooth


logger = logging.getLogger(__name__)

class Command():
	Attention = 'AT'
	End = '\n'
	Error = 'ER'
	Okay = 'OK'
	# Info = 'HI'
	SetMode = 'SM'
	# GetMode = 'GM'
	SetRGB = 'SV' # (for Set Values)
	# GetRGB = 'GV' # (for Get Values)
	SetSpeed = 'SS'
	ToggleOnboardLED = 'TL'

	class Mode():
		"""To be used after SetMode"""
		Steady = 'STD'
		Blink = 'BLK'
		Pulse = 'PLS'

# class Responses():
# 	Error = 'ER'
# 	Okay = 'OK'

# class Command():
# 	Attention = 0x30
# 	End = 31
# 	Info = 32
# 	DestroyTheJedi = 66
# 	SetMode = 33
# 	GetMode = 34
# 	SetRGB = 0x35
# 	GetRGB = 36

# 	class Mode():
# 		"""To be used after SetMode"""
# 		Steady = 37
# 		Blink = 38
# 		Pulse = 39


class Notifier():

	def __init__(self, device_prefix='ESP32test', port=1):
		self.device_prefix = device_prefix
		self._sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self._port = port

	def discover(self, duration=4):
		nearby = bluetooth.discover_devices(
			duration=duration, lookup_names=True, flush_cache=True)

		print('Found devices', nearby)
		# logger.warn('Found devices', nearby)

		for addr, name in nearby:
			if name.startswith(self.device_prefix):
				return addr, name

		raise Exception('Could not find notifier')

	def connect(self, addr, port=1):
		# TODO: make sure any old connection is cleared first
		self._sock.connect((addr, port))

	# def command(self, *commands):
	# 	self._sock.sendall(Command.Attention)

	# 	for command in commands:
	# 		self._sock.sendall(command)

	# 	self._sock.sendall(Command.End)

	def command(self, *commands):
		# the format is as follows:
		# 	Attention: AT
		#   message length including attention and length byte
		#   command and data
		#   END: \n
		command = ''.join(commands)
		message = Command.Attention
		message += chr(len(command) + 3) # +3 for AT and length bit
		message += command
		message += Command.End

		# print('command: %s' % message)
		self._sock.sendall(message)

		# for command in commands:
		# 	self._sock.sendall(command)

		# self._sock.sendall(Command.End)
		return self.readUntil('\n')


	# def read(self):
	# 	message = ''
	# 	while True:
	# 		data = self._sock.recv(2)
	# 		print('data: "%s"' % data)
	# 		if :
	# 			break
	# 		message += data
	# 	# message = self._sock.recv(2)
	# 	print('message: "%s"' % message)
	# 	return message

	def readUntil(self, end):
		message = ''
		while True:
			char = self._sock.recv(1)

			if char == end:
				if message != 'OK':
					print('message: "%s"' % message)
				return message

			message += char

	# def read(self):
	# 	time.sleep(0.01)
	# 	message = self._sock.recv(2048)
	# 	print('message: "%s"' % message)
	# 	return message

	def hello(self):
		self.command(Command.Info)

	def set_rgb(self, red, green, blue):
		return self.command(Command.SetRGB, red, green, blue)

	def set_mode(self, mode):
		return self.command(Command.SetMode, mode)

	def set_speed(self, speed):
		return self.command(Command.SetSpeed, str(speed))






# def main():

# 	print("performing inquiry...")

# 	nearby_devices = bluetooth.discover_devices(
# 	    duration=8, lookup_names=True, flush_cache=True)

# 	print("found %d devices" % len(nearby_devices))

# 	device_addr = None
# 	device_name = None

# 	for addr, name in nearby_devices:
# 		if name == 'ESP32test':
# 			device_addr = addr
# 			device_name = name

# 		try:
# 		    print("  %s - %s" % (addr, name))
# 		except UnicodeEncodeError:
# 		    print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))

# 	if device_addr is None:
# 		print("no test device found")
# 		sys.exit(1)

# 	service_matches = bluetooth.find_service(address=device_addr)

# 	first_match = service_matches[0]
# 	port = first_match["port"]
# 	name = first_match["name"]
# 	host = first_match["host"]

# 	print(first_match)
# 	print("connecting to \"%s\" on %s (port %s)" % (device_name, host, port))

# 	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# 	# sock.connect((host, port))
# 	sock.connect(('CC:50:E3:A9:1F:72', 1))

# 	print("connected.  type stuff")
# 	sock.send('Hello World')
# 	while True:
# 		data = raw_input()

# 		if len(data) == 0:
# 			break

# 		sock.send(data)

# 	sock.close()

if __name__ == '__main__':
	# main()
	notifier = Notifier()
	addr, name = notifier.discover(2)
	notifier.connect(addr)
	# notifier.hello()
	# notifier.command(Command.SetRGB, '1')
	# time.sleep(1)
	# notifier.command(Command.SetRGB, '0')
	notifier.set_mode(Command.Mode.Steady)
	# notifier.set_speed(2000)

	# while True:
	for i in range(0, 256):
		notifier.set_rgb("{:02x}".format(i), "{:02x}".format(255 - i), '00')
		# time.sleep(0.01)

	for i in range(0, 256):
		notifier.set_rgb("{:02x}".format(255 - i), '00', "{:02x}".format(i))
		# time.sleep(0.02)

	for i in range(0, 256):
		notifier.set_rgb('00', "{:02x}".format(i), "{:02x}".format(255 - i))
		# time.sleep(0.02)

		# for i in range(0, 256, 2):
		# 	notifier.set_rgb('00', "{:02x}".format(255 - i), '00')
		# 	time.sleep(0.01)

	# notifier.set_rgb('FF', '00', '00')
	# time.sleep(1)
	# notifier.set_rgb('00', 'FF', '00')
	# time.sleep(1)
	# notifier.set_rgb('00', '00', '55')
	# time.sleep(1)
	# notifier.set_rgb('00', '00', '00')
	# notifier.set_mode(Command.Mode.Blink)
	# notifier.set_rgb('00', '00', 'FF')
	# time.sleep(5)
	# notifier.set_rgb('FF', '00', 'FF')
	# time.sleep(5)
	# notifier.set_rgb('99', '66', '66')
	# time.sleep(5)

	notifier.set_rgb('00', '00', '00')
