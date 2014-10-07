from bluetooth import *

__author__ = 'Rohit'

# Server inits
# btport = 4					# RFCOMM port 4

class AndroidAPI(object):

	def __init__(self):
		"""
		Connect to Nexus 7
		RFCOMM port: 4
		Nexus 7 MAC address: 08:60:6E:A5:82:C8
		"""
		self.server_socket = None
		self.client_socket = None
		self.bt_is_connected = False
		btport = 4

		# Creating the server socket and bind to port		
		self.server_socket = BluetoothSocket( RFCOMM )
		self.server_socket.bind(("", btport))
		self.server_socket.listen(1)	# Listen for requests
		self.port = self.server_socket.getsockname()[1]
		uuid = "00001101-0000-1000-8000-00805F9B34FB"

		advertise_service( self.server_socket, "SampleServer",
		                   service_id = uuid,
		                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
		                   profiles = [ SERIAL_PORT_PROFILE ],
						)

	def close_bt_socket(self):
		"""
		Close socket connections
		"""
		if self.client_socket:
			self.client_socket.close()
			print "Closing client socket"
		if self.server_socket:
			self.server_socket.close()
			print "Closing server socket"
		self.bt_is_connected = False


	def bt_is_connect(self):
		"""
		Check status of BT connection
		"""
		return self.bt_is_connected


	def connect_bluetooth(self):
		"""
		Connect to the Nexus 7 device
		"""
		print "Waiting for connection on RFCOMM channel %d" % self.port
		# Accept requests
		self.client_socket, client_address = self.server_socket.accept()
		print "Accepted connection from ", client_address
		self.bt_is_connected = True


	def write_to_bt(self, message):
		"""
		Write message to Nexus
		"""
		try:
			self.client_socket.send(str(message))
		except BluetoothError:
			print "Bluetooth Error. Connection reset by peer"
			self.connect_bluetooth()	# Reestablish connection
		# print "Send to Android: %s " % message
		# return True

			
	def read_from_bt(self):
		"""
		Read incoming message from Nexus
		"""
		# while self.bt_is_connect():
		try:
			msg = self.client_socket.recv(1024)
			print "Received [%s] " % msg
			return msg
		except BluetoothError:
			print "Bluetooth Error. Connection reset by peer. Trying to connect"
			self.connect_bluetooth()	# Reestablish connection
		
		# return msg


# if __name__ == "__main__":
# 	print "Running Main"
# 	bt = AndroidAPI()
# 	bt.init_bluetooth()
	
# 	send_msg = raw_input()
# 	print "Write(): %s " % send_msg
# 	bt.write_to_bt(send_msg)

# 	#print "read"
# 	# print "data received: %s " % bt.read_from_bt()

# 	print "closing sockets"
# 	bt.close_bt_socket()

