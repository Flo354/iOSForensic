#!/usr/bin/python
# -*- coding: utf8 -*-

#Copyright (C) <2014>  <Florian Pradines>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from subprocess import Popen, PIPE, STDOUT
import getopt
import sys

from general import *
from package import *

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ahvi:p:P:", ["about", "help", "verbose", "ip=", "port=", "password="])
	except getopt.GetoptError, err:
		print err
		help()
		sys.exit()

	ip 			= False
	port 		= "22"
	password 	= "alpine"
	verbose 	= False
	
	#Parse options
	for opt, arg in opts:
		if opt in ("-a", "--about"):
			about()
			sys.exit()
		elif opt in ("-h", "--help"):
			help()
			sys.exit()
		elif opt in ("-v", "--verbose"):
			verbose = True
		elif opt in ("-i", "--ip"):
			ip = arg
		elif opt in ("-p", "--port"):
			port = str(arg)
		elif opt in ("-P", "--password"):
			password = arg
	
	if not ip:
		print "Error : you must give the local ip address of the device"
		help()
		sys.exit()
	
	print "Test connection to the device"
	cmd = "sshpass -p " + password + " ssh root@" + ip + " -p " + port + " -oStrictHostKeyChecking=no echo ok"
	process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
	stdout, stderr = process.communicate()
	if stdout.replace("\n", "").replace("\r", "")[-2:] != "ok":
		print "Error : " + stdout
		sys.exit()
	print "Connection successful"
	print ""

	print "Searching packages"
	found = []
	if len(args) is 0:
		args.append("")
	
	for arg in args:
		if arg[-4:] == ".app":
			arg = arg[:-4]
		
		package 	= Package(ip, port, password, arg, verbose)
		justFound 	= package.find()
		
		if justFound:
			found = removeDuplicates(found + justFound)

	if not found:
		print "no packages found"
		sys.exit()
	
	i = 1	
	for package in found:
		print str(i) +") "+ package.split("/", 1)[1].replace(".app", "")
		i += 1

	choices = raw_input("Which packages do you want extract. Ex: 1 3 6 (type 0 to quit) : ").split()
	if choices[0] is "0":
		sys.exit()
				
	packages = []
	for choice in map(int,choices):
		if choice < 1 or choice > len(found):
			print str(choice) + " is not a good value"
		else:
			packages.append(found[choice - 1])
	
	for package in packages:	
		print ""
		print ""
		
		if package[-4:] == ".app":
			package = package[:-4]
	
		package = Package(ip, port, password, package, verbose)
		package.extract()

if __name__ == "__main__":
	main ()
