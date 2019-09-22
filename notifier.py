import logging
import time

import bluetooth

from command import Command

logger = logging.getLogger(__name__)


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
    #   self._sock.sendall(Command.Attention)

    #   for command in commands:
    #       self._sock.sendall(command)

    #   self._sock.sendall(Command.End)

    def command(self, *commands):
        # the format is as follows:
        #   Attention: AT
        #   message length including attention and length byte
        #   command and data
        #   END: \n
        command = ''.join(commands)
        message = Command.Attention
        message += chr(len(command) + 3) # +3 for AT and length bit
        message += command
        message += Command.End

        # print('command: %s' % message)
        self._sock.send(message)

        # for command in commands:
        #   self._sock.sendall(command)

        # self._sock.sendall(Command.End)
        return self.readUntil('\n')


    # def read(self):
    #   message = ''
    #   while True:
    #       data = self._sock.recv(2)
    #       print('data: "%s"' % data)
    #       if :
    #           break
    #       message += data
    #   # message = self._sock.recv(2)
    #   print('message: "%s"' % message)
    #   return message

    def readUntil(self, end):
        message = ''
        while True:
            char = self._sock.recv(1).decode('utf-8')

            if char == end:
                if message != 'OK':
                    print('message: "%s"' % message)
                return message

            message += char

    # def read(self):
    #   time.sleep(0.01)
    #   message = self._sock.recv(2048)
    #   print('message: "%s"' % message)
    #   return message

    def hello(self):
        self.command(Command.Info)

    def set_rgb(self, red, green, blue):
        return self.command(Command.SetRGB, red, green, blue)

    def set_mode(self, mode):
        return self.command(Command.SetMode, mode)

    def set_speed(self, speed):
        return self.command(Command.SetSpeed, str(speed))
