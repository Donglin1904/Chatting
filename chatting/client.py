import socket
import threading
import pygame
import sys
from time import sleep
from words import Words

class Chatting:

	def __init__(self):
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.host=input('host(nothing means 192.168.3.11)')
		if self.host == '':
			self.host='192.168.3.11'
		try:
			self.sock.connect((self.host,56295))
		except socket.gaierror:
			print('host wrong')
			self.sock.close()
			sys.exit()
		
		self.sock.send('connect'.encode('ascii'))
		print('正在连接服务器')
		self.sock.settimeout(10)
		try:
			self.sock.recv(1024)
		except socket.timeout:
			print('服务器连接失败')
			self.sock.close()
			sys.exit()
		except ConnectionResetError:
			print('服务器未开启')
			self.sock.close()
			sys.exit()
		else:
			print('服务器连接成功')
			self.sock.settimeout(None)
			sleep(1)
		self.id=input('your id :')

		pygame.init()
		self.screen=pygame.display.set_mode((1200,650))
		pygame.display.set_caption('chatting')

		self.words=pygame.sprite.Group()

		self.thread1=threading.Thread(target=self.write)
		self.thread1.setDaemon(True)
		self.thread1.start()

		self.thread2=threading.Thread(target=self.recive)
		self.thread2.setDaemon(True)
		self.thread2.start()

		self.active=True

	def write(self):
		while True:
			self.write=input('write what you want to say: ')
			self.sock.send(f'{self.id}: {self.write}'.encode('ascii'))

	def recive(self):
		while True:
			self.data=self.sock.recv(1024)
			self.data=self.data.decode('ascii')
			if self.data == 'end':
				self.sock.close()
				sys.exit()
			self.new_words=Words(self)
			for words in self.words:
				words.move()
				if words.words_rect.y <= 0:
					self.words.remove(words)
			self.words.add(self.new_words)

	def run(self):
		while self.active:
			self.check_event()
			self.update_screen()

	def check_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.sock.send('end'.encode('ascii'))
				self.active=False

	def update_screen(self):
		self.screen.fill((230,230,230))

		for word in self.words.sprites():
			word.draw_words()

		pygame.display.flip()
		pygame.time.Clock().tick(60)

if __name__ == '__main__':
	main=Chatting()
	main.run()