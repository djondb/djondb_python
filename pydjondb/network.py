import socket
import struct
from defs import *

def long_fromendian(buffer, pos):
	res =struct.unpack_from('<q', buffer, pos)
	return res[0]

def int_fromendian(buffer, pos):
	res =struct.unpack_from('<i', buffer, pos)
	return res[0]

def double_fromendian(buffer, pos):
	res =struct.unpack_from('<d', buffer, pos)
	return res[0]

def long_toendian(val):
	res =struct.pack('<q', val)
	return res

def int_toendian(val):
	res = struct.pack('<i', val)
	return res

def double_toendian(val):
	res = struct.pack('<i', val)
	return res

class Network:
	def __init__(self):
		self.buffer = bytearray()
		self.bufferLen = 0
		self.bufferPos = 0

	def connect(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))

	def writeString(self, data):
		self.writeInt(len(data))
		self.buffer.extend(data.encode('utf-8').strip())
		self.bufferLen += len(data)

	def writeInt(self, val):
		self.buffer.extend(int_toendian(val))
		self.bufferLen += 4

	def writeBool(self, val):
		self.checkBuffer(1)
		if val is True:
			self.buffer.append(1)
		else:
			self.buffer.append(0)
		self.bufferPos += 1 

	def writeDouble(self, val):
		self.buffer.extend(double_toendian(val))
		self.bufferLen += 8 

	def writeLong(self, val):
		self.buffer.extend(long_toendian(val))
		self.bufferLen += 8

	def writeBSON(self, data):
		self.writeLong(len(data))
		for key in data.keys():
			self.writeString(key.encode('utf-8').strip())
			val = data[key]
			isSet = False
			if type(val) is int:
				self.writeLong(0)
				self.writeInt(val)
				isSet = True

			if type(val) is float:
				self.writeLong(1)
				self.writeDouble(val)
				isSet = True

			if type(val) is long:
				self.writeLong(2)
				self.writeLong(val)
				isSet = True

			if type(val) is str:
				self.writeLong(4)
				self.writeString(val)
				isSet = True

			if type(val) is unicode:
				self.writeLong(4)
				self.writeString(val.encode('utf-8').strip())
				isSet = True

			if type(val) is dict:
				self.writeLong(5)
				self.writeBSON(val)
				isSet = True

			if type(val) is bool:
				self.writeLong(10)
				self.writeBool(val)
				isSet = True

			if not isSet:
				raise DjondbException(601, 'Unsupported datatype %s' % type(val)) 

	def readBSONArray(self):
		elements = self.readLong()
		result = []
		for x in range(0, elements):
			result.append(self.readBSON())
		return result

	def readBSON(self):
		elements = self.readLong()
		result = {}
		for x in range(0, elements):
			key = self.readString()
			datatype = self.readLong()
			val = None
			if datatype is 0:
				val = self.readInt()
			if datatype is 1:
				val = self.readDouble()
			if datatype is 2:
				val = self.readLong()
			if datatype is 4:
				val = self.readString()
			if datatype is 5:
				val = self.readBSON()
			if datatype is 6:
				val = self.readBSONArray()
			if datatype is 10:
				val = self.readBoolean()
			result[key] = val
		return result

	def readChar(self):
		self.checkBuffer(1)
		c = self.buffer[self.bufferPos]
		self.bufferPos += 1
		return chr(c)

	def readBoolean(self):
		self.checkBuffer(1)
		res = self.buffer[self.bufferPos] is 1
		self.bufferPos += 1 
		return res

	def readInt(self):
		self.checkBuffer(4)
		res = int_fromendian(self.buffer, self.bufferPos)
		self.bufferPos += 4
		return res

	def readLong(self):
		self.checkBuffer(8)
		res = long_fromendian(self.buffer, self.bufferPos)
		self.bufferPos += 8 
		return res

	def readDouble(self):
		self.checkBuffer(8)
		res = double_fromendian(self.buffer, self.bufferPos)
		self.bufferPos += 8 
		return res

	def readString(self):
		size = self.readInt()
		self.checkBuffer(size)
		result = ""
		for x in range(0, size):
			result += self.readChar()
		return result

	def waitAvailable(self):
		if (self.bufferPos >= self.bufferLen):
			self.buffer.extend(self.socket.recv(1024*100))
			self.bufferLen = len(self.buffer)

	def checkBuffer(self, size):
		if (self.bufferLen < (self.bufferPos + size)):
			self.waitAvailable()

	def reset(self):
		self.buffer = bytearray()
		self.bufferLen = 0
		self.bufferPos = 0

	def flush(self):
		self.socket.sendall(self.buffer)
		self.reset()

