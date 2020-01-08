# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         check_atc.py
# Purpose:      Check the AT Command to target device correspond
# Author:       Ryosuke Uematsu
# History:      2019/12/13 v1.0 Created
#-------------------------------------------------------------------------------
import serial
import sys
import os
import time
from atc_list import *
import binascii

baud_rate_list=[
	"75",
	"110",
	"134.5",
	"150",
	"300",
	"600",
	"1200",
	"1800",
	"2400",
	"4800",
	"7200",
	"9600",
	"14400",
	"19200",
	"31250",
	"38400",
	"56000",
	"57600",
	"76800",
	"115200",
	"128000",
	"230400",
	"256000"
]

def main():
	device_name = "" #default
	baud_rate = "115200" #default
	atc_test = []
	print "Check AT Command v1.0"

 	if(len(sys.argv)>1):
		for i in range(1,len(sys.argv)):
			if sys.argv[i]=="-h":
				print "Usage: check_atc.py [Options]"
				print "Options:"
				print " -h :help command"
				print " -d <device name> :device name ex./dev/ttyACM0"
				print " -s <baud rate>:baud rate (default=115200)"
				print "ATCommand Options:"
				for option in atc_option.keys():
					print " " + option + " : " + atc_option[option][0]
				sys.exit()
			elif sys.argv[i]=="-d":
				if len(sys.argv)>=i+2:
					if os.system("ls "+sys.argv[i+1])==0:
						device_name = sys.argv[i+1]
					else:
						print "error:device name invalid!"
						sys.exit()
				else:
					print "error:device name invalid!"
					sys.exit()
			elif sys.argv[i]=="-s":
				if len(sys.argv)>=i*2:
					if sys.argv[i*2] in baud_rate_list:
						baud_rate = sys.argv[i*2]
					else:
						print "error:baud_rate invalid!"
						sys.exit()
				else:
					print "error:baud_rate invalid!"
					sys.exit()
			elif sys.argv[i] in atc_option.keys():
				atc_test.append(sys.argv[i])
			else:
				pass

	else:
		print "Usage: check_atc.py [Options]"
		print "Options:"
		print " -h :help command"
		print " -d <device name> :device name ex./dev/ttyACM0"
		print " -s <baud rate>:baud rate (default=115200)"
		print "ATCommand Options:"
		for option in atc_option.keys():
			print " " + option + " : " + atc_option[option][0]

		sys.exit()

	print "Device Name:"+device_name
	print "Baud Rate:"+	baud_rate
	ser = serial.Serial(device_name,baud_rate)
	ser.write("AT\r")

	read_message = ""
	while 1:
		str_r = ser.read(1)
		read_message = read_message + str_r
		if read_message.find("OK")!=-1:
			break
		else:
			pass

	print "---------------------------------"
	print "AT Command\tResult"
	print "---------------------------------"
	for atc in atc_test:
		print "********* " + atc_option[atc][0] +" ***********"
		for command in atc_option[atc][1]:
			ser.write(command+"\r")
			#print "Send:" + command + "\r"
			read_message = ""
			while 1:
				str_r = ser.readline().replace("\r","").replace("\n","")
				#print "log:" +  str_r
				#print "log hex:" +  binascii.b2a_hex(str_r)
				if str_r.find(command)!=-1:
					read_message = ""
				elif str_r=="" or str_r=="\r" or str_r=="\n" or str_r=="\r\n" or str_r=="\n\r":
					pass
				elif str_r.find("OK")!=-1:
					read_message = read_message + str_r + "\r"
					break
				elif str_r.find("ERROR")!=-1:
					read_message = read_message + str_r + "\r"
					break
				elif str_r.find("CONNECT")!=-1:
					read_message = read_message + str_r + "\r"
					break
				elif str_r.find(command.split("AT")[0])!=-1 and command.split("AT")[0]!="":
					read_message = read_message + str_r
					break
				elif str_r.find("NO CARRIER")!=-1:
					read_message = read_message + str_r + "\r"
					break
				else:
					read_message = read_message + str_r + "\r"


			if len(command) < 8:
				print command + "\t\t"+read_message.split("\r")[-2]
			else:
				print command + "\t"+read_message.split("\r")[-2]

	ser.close()

if __name__ == '__main__':
    main()
