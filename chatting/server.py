import socket

class Server:

	def __init__(self):
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.host=input('host:')
		if self.host == '':
			self.host='192.168.3.11'
		try:
			self.sock.bind((self.host,56295))
		except socket.gaierror:
			print('host wrong')
			self.sock.close()
			exit()

		self.save=[]

	def connect(self):
		while True:
			self.data,self.address=self.sock.recvfrom(1024)
			self.data=self.data.decode('ascii')
			if self.data == 'end':
				self.sock.sendto('end'.encode('ascii'),self.address)
				if self.address in self.save:
					self.save.remove(self.address)
				continue
			elif self.data == 'connect':
				self.sock.sendto('connect'.encode('ascii'),self.address)
				self.save.append(self.address)
				continue
			for address in self.save:
				self.sock.sendto(self.data.encode('ascii'),address)

if __name__ == '__main__':
	main=Server()
	main.connect()
