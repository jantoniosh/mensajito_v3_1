# -*- coding: utf-8 -*-
# Clase para control de acciones de Radio con Raspberry
# mensajito.mx
# Idea Original : Diego Aguirre
# Código: Antonio Salinas

import os
import sys
import subprocess as sub
import xml.etree.ElementTree as ET
import time
import urllib2
import ConfigParser
import commands

class radio_class:

	bro_flag = False	# Flag -- BROADCAST
	int_flag = False	# Flag -- INTERNET
	aud_flag = False	# Flag -- AUDIO
	usb_flag = False 	# Flag -- USB
	mount_Point = ''	# Broadcast Link
	name 		= ''	# Broadcast Name
	location 	= ''	# Broadcast Location
	description = ''	# Broadcast Description
	genre 		= '' 	# Broadcast genre
	mp3_file	= ''
	listeners = 0
	socket = ''
	conn = ''
	ip = ''
	memoria = ''
	socket = ''

	# Class Constructor
	def __init__(self, socket):
		self.socket 		= socket
		# Get Mount Point
		self.gen_mountPoint()
		self.get_ip()
		# Default Data
		self.name 		= 'mensajito'
		self.location		= 'mensajito'
		self.description	= 'mensajito'
		self.genre 		= 'mensajito'
		self.tags		= ''
		self.count_fail		= 0

	def gen_mountPoint(self):
		proc = sub.Popen('cat /sys/class/net/eth0/address', shell=True, stdout=sub.PIPE, )
		phy_add=proc.communicate()[0]
		add_phy = phy_add[::-1]
		add_phy = add_phy.split('\n')
		self.mount_Point = add_phy[1].replace(':','')
		print self.mount_Point
		return self.mount_Point

	def get_mountPoint(self):
		msg = "mou@" + self.mount_Point
		self.socket.sendto(msg, ('localhost', 6000))

	def get_ip(self):
		ip = commands.getoutput('hostname -I')
		self.ip = ip.split(' ')[0]
		msg = "ip@" + self.ip
                self.socket.sendto(msg, ('localhost', 6000))
		print self.ip

	def get_data(self):
		file = open("/home/pi/config/data.txt", "r")
		data = file.read()
		name = data.split('\n')[0]
		location = data.split('\n')[1]
		self.name = name
		self.location = location

	def get_memoria(self):
		free = os.popen("df -h")
		for i in range(0, 1):
			if i == 1:
				line = free.readline()
				line_split = line.split()
				print line_split
				self.memoria = line_split[3]

	def get_internet(self):
                msg = "int@" + str(int(self.int_flag))
                self.socket.sendto(msg, ('localhost', 6000))

	def get_audio(self):
		msg = "aud@" + str(int(self.aud_flag))
                self.socket.sendto(msg, ('localhost', 6000))

	def get_nombre(self):
		msg = "nom@" + self.name
                self.socket.sendto(msg, ('localhost', 6000))

	def get_ubicacion(self):
		msg = "ubi@" + self.location
                self.socket.sendto(msg, ('localhost', 6000))

	def internet_connect(self):
		ping = os.system('sudo timeout 0.25 ping -c1 8.8.8.8 > /dev/null')
		nb_ping = not(bool(ping))
		# print nb_ping
		if ping == 0:
			self.count_fail = 0
			self.internet_up()
		else:
			self.count_fail = self.count_fail + 1
			if self.count_fail >= 10:
				print '\nSin Internet'
				self.internet_down()
		# print self.count_fail
		return ping

	def internet_up(self):
		self.int_flag = True
		return self.int_flag

	def internet_down(self):
		self.int_flag = False
		# Método que termina transmisión
		self.stop_transm()
		return self.int_flag

	def audio_device(self):
		a_dev = os.popen('arecord -l')
		line_t = a_dev.read()
		line = line_t.split('\n')
		n_lines = len(line)
		if n_lines == 2:
			print '\nNo se encuentra dispositivo de audio'
			self.audio_down()
		elif n_lines == 5:
			self.audio_up()
		return n_lines

	def audio_up(self):
		self.aud_flag = True
		return self.aud_flag

	def audio_down(self):
		self.aud_flag = False
		return self.aud_flag

	def mp3_date(self):
		date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		self.mp3_file = '/home/pi/audio/%s.mp3' %date
		return self.mp3_file

	def cfg_darkice(self):
		self.mp3_date()
		os.system('sudo rm /etc/darkice.cfg')
		Config = ConfigParser.ConfigParser()
		Config.optionxform = str
		cfgfile = open("/home/pi/mensajito_back/data/aux_cfg",'w')
		Config.add_section('general')
		Config.add_section('input')
		Config.add_section('icecast2-0')
		# [general]
		Config.set('general', 'duration', 0)
		Config.set('general', 'bufferSecs', 60)
		Config.set('general', 'reconnect', 'yes')
		# [input]
		Config.set('input', 'device', 'mensajito')
		Config.set('input', 'sampleRate', 48000)
		Config.set('input', 'bitsPerSample', 16)
		Config.set('input', 'channel', 2)
		# [icecast2-0]
		Config.set('icecast2-0', 'bitrateMode', 'vbr')
		Config.set('icecast2-0', 'bitrate', 128)
		Config.set('icecast2-0', 'format', 'mp3')
		Config.set('icecast2-0', 'quality', 0.6)
		Config.set('icecast2-0', 'server', 'mensajito.mx')
		Config.set('icecast2-0', 'port', 8000)
		Config.set('icecast2-0', 'password', 'mensajito$1192')
		Config.set('icecast2-0', 'mountPoint', self.mount_Point)
		Config.set('icecast2-0', 'sampleRate', 48000)
		Config.set('icecast2-0', 'channel', 2)
		Config.set('icecast2-0', 'name', self.name)
		Config.set('icecast2-0', 'description', self.description)
		Config.set('icecast2-0', 'genre', self.genre)
		Config.set('icecast2-0', 'public', 'yes')
		# Config.set('icecast2-0', 'localDumpFile', self.mp3_file)
		# Write the changes
		Config.write(cfgfile)
		cfgfile.close()
		os.system("sudo cp /home/pi/mensajito_back/data/aux_cfg /etc/darkice.cfg")
		os.system("sudo rm /home/pi/mensajito_back/data/aux_cfg")

	def n_listeners(self):
		try:
			str_listen = ''
            		url = 'http://mensajito.mx:8000/' + self.mount_Point + '.xspf'
			f = urllib2.urlopen(url)
			data = f.read()
			data_split = data.split('\n')
			aux_listen = data_split[12].split(':')
			self.listeners = int(aux_listen[1])
		except:
			self.listeners = 0
		self.socket.sendto("lis@" + str(self.listeners), ('localhost', 6000))
		return self.listeners



	def start_transm(self):
		if self.int_flag == True and self.aud_flag == True:
			self.bro_flag = True
			self.get_data()
			self.cfg_darkice()
			os.system("darkice &")
			cmd = 'arecord -f dat --device="mensajito" - | lame - ' + self.mp3_file + " &"
			#cmd = 'arecord --format S16_LE --rate 44100 --device="mensajito" - | lame - ' + self.mp3_file + " &"
			print(cmd)
			os.system(cmd)

	def stop_transm(self):
		if self.aud_flag == True:
			self.bro_flag = False
			os.system('sudo killall darkice')
			os.system('sudo killall arecord')
			self.socket.sendto("err@1", ('localhost', 6000))

