import os
import MySQLdb
import time

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


while 1:
	size, avail, percent = getFree()
	update_mem = "UPDATE datos_generales SET memoria = '%s' WHERE id = 1" %avail
	print update_mem
	run_query(Conn, update_mem)
	time.sleep(2)
