#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import Popen, PIPE, STDOUT
import sys

def about():
	print "####################################################"
	print "#	@author		Florian Pradines	   #"
	print "#	@company	Phonesec		   #"
	print "#	@mail		f.pradines@phonesec.com	   #"
	print "#	@mail		florian.pradines@owasp.org #"
	print "#	@version	2.0			   #"
	print "#	@licence	GNU GPL v3		   #"
	print "#	@dateCreation	20/05/2014		   #"
	print "#	@lastModified	23/05/2014		   #"
	print "####################################################"
	print ""
	print "iosForensic is a python tool to help in forensics analysis on iOS."

def help():
	print "Usage : "+ sys.argv[0] +" [OPTIONS] APP_NAME.app INCOMPLETE_APP_NAME APP_NAME2_WITHOUT_DOT_APP"
	print "-h --help : show help message"
	print "-a --about : show informations"
	print "-v --verbose : verbose mode"
	print "-i --ip : local ip address of the iOS terminal"
	print "-p --port : ssh port of the iOS terminal (default 22)"
	print "-P --password : root password of the iOS terminal (default alpine)"
	print ""
	print "Examples"
	print sys.argv[0] + "-i 192.168.1.10 [OPTIONS] APP_NAME.app INCOMPLETE_APP_NAME APP_NAME2_WITHOUT_DOT_APP"
	print sys.argv[0] + "-i 192.168.1.10 -p 1337 -P pwd MyApp.app angry MyApp2"

	
def printVerbose (process):
	while process.poll() is None:
		print process.stdout.readline().replace("\n", "").replace("\r", "")
	process.communicate()

def writeResultToFile (cmd, filename, verbose):
	try:
		f = open(filename, "w")
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		
		while True:
			line = process.stdout.readline()
			if not line:
				break
			
			f.write(line)
			
			if verbose:
				print line.replace("\n", "").replace("\r", "")
		
		process.communicate()
		f.close()
		
		return True
	except IOError as e:
		print "File " + e.filename +" not created"
		print "Exception : "+ e.strerror

def removeDuplicates (seq):
	seen = set()
	seen_add = seen.add
	return [ x for x in seq if x not in seen and not seen_add(x)]
