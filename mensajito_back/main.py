# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# mensajito -- Main Program
# mensajito.mx
# Idea Original : Diego Aguirre
# Código: Antonio Salinas

import time
import threading
import os
import radio.radio_ctrl as radio
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 6100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


def do_chk(radio):
	global end
        while 1:
		try:
			radio.internet_connect()
                        radio.audio_device()
                except KeyboardInterrupt:
                    	end = True
		except Exception as e:
			print e
		if end == True:
			break

		time.sleep(2)

def do_escuchas(radio):
	global end
	while 1:
                try:
                        radio.n_listeners()
			radio.get_internet()
			radio.get_audio()
                except KeyboardInterrupt:
                        end = True
                except Exception as e:
                        print e
                if end == True:
                        break
		time.sleep(2)

def getFree():
        free = os.popen("df -h")
        i = 0
        while True:
                i = i + 1
                line = free.readline()
                print line
                if i==2:
                        line_split = line.split()
                        return(line_split[1], line_split[3], line_split[4])


if __name__ == '__main__':
	global end
	global data
	try:
		end = False
		r_tm = radio.radio_class(sock)
		#d_m = threading.Thread(target = do_memoria, args = (r_tm,))
		d_chk = threading.Thread(target = do_chk, args = (r_tm,))
		#d_a = threading.Thread(target = do_audio, args = (r_tm,))
		d_e = threading.Thread(target = do_escuchas, args = (r_tm,))

		#d_m.start()
		d_chk.start()
		#d_a.start()
		d_e.start()

		while 1:
			# Espera para transmitir
			data, addr = sock.recvfrom(1024)
			print data
			if data == "nom":
				print "obtener nombre"
				r_tm.get_nombre()
			elif data == "ubi":
				print "obtener ubicacion"
				r_tm.get_ubicacion()
			elif data == "mou":
				print "obtener mount point"
				r_tm.get_mountPoint()
			elif data == "ip":
				print "obtener ip"
				r_tm.get_ip()
			elif data == "int":
				print "obtener internet"
				r_tm.get_internet()
			elif data == "aud":
				print "obtener audio"
				r_tm.get_audio()
			elif data == "tr":
				r_tm.start_transm()
			elif data == "st":
				r_tm.stop_transm()
			elif data == "mem":
				size, avail, percent = getFree()
				sock.sendto("mem@" + avail, ('localhost', 6000))

	except KeyboardInterrupt:
		end = True
		print 'Fin del Programa'
