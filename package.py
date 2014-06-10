#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import Popen, PIPE, STDOUT
import os
import sys
import datetime
import time
import fnmatch
import magic

from general import *

class Package():
	def __init__(self, ip, port, password, package, verbose):
		self.package 	= package
		self.appname 	= False
		self.verbose 	= verbose
		self.basepath 	= "/var/mobile/Applications/"
		self.basecmd 	= "sshpass -p " + password + " "
		self.basesshcmd = self.basecmd + "ssh root@" + ip + " -p " + port + " "
		self.basescpcmd = self.basecmd + "scp -r -v -P " + port + " root@" + ip + ":" + self.basepath

	def find(self):
		cmd = self.basesshcmd + "find -L " + self.basepath + " -iname *" + self.package + "*.app -type d -prune"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		stdout, stderr = process.communicate()
		if stdout == "":
			return False
		else:
			return stdout.replace(self.basepath, "").split()

	def extract(self):
		self.appname = self.package.split("/", 1)[1].replace(".app", "")
		self.package = self.package.split("/", 1)[0]

		self.createDirectories()
		if self.verbose: print ""
		
		self.getDatas()
		if self.verbose: print ""
		
		self.getSQL()
		if self.verbose: print ""
		
		self.getPlist()
		if self.verbose: print ""
		
		self.getLogs()
		
		return True
		
	def createDirectories(self):
		try:
			self.path = "output/"+ self.appname
			if os.path.exists (self.path):
				self.path = "output/"+ self.appname +"-"+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
			
			self.pathData 	= self.path + "/data"
			self.pathSQL 	= self.path + "/SQL"
			self.pathPlist 	= self.path + "/plist"
			
			if not self.verbose:
				print "Creating directories..."
			
			if self.verbose:
				print "Creating directory : " + self.pathData
			os.makedirs(self.pathData)
			if self.verbose:
				print "Creating directory : "+ self.pathSQL
			os.makedirs(self.pathSQL)
			if self.verbose:
				print "Creating directory : "+ self.pathPlist
			os.makedirs(self.pathPlist)
		except OSError as e:
			print "Folder " + e.filename +" not created"
			print "Exception : "+ e.strerror
	
	def getDatas(self):
		print "Downloading datas..."

		cmd = self.basescpcmd + "/" + self.package + "/* " + self.pathData
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
	
	def getSQL(self):
		print "Finding databases files..."
		mime = magic.Magic()
		for root, dirnames, filenames in os.walk(self.pathData):
		  for filename in fnmatch.filter(filenames, "*"):
		  	try:
			  	typeFile = mime.from_file(root +"/"+ filename)
				if typeFile is not None and typeFile.find("SQLite", 0, 6) is not -1:
				  	if self.verbose:
				  		print "Database found : "+ root +"/"+ filename
				  	
				  	os.makedirs(self.pathSQL + "/" + filename)
				  	
				  	cmd = "sqlite3 "+ root +"/"+ filename +" .tables"
				  	process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
				  	stdout, stderr = process.communicate()

				  	cmd = "sqlite3 "+ root +"/"+ filename
					process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
					process.stdin.write(".headers on\n")
					process.stdin.write(".mode csv\n")
				  	for table in stdout.split():
				  		if self.verbose:
				  			print "\tExtracting table : "+ table
						process.stdin.write(".output "+ self.pathSQL +"/"+ filename +"/"+ table +".csv\n")
						process.stdin.write("select * from "+ table +";\n")
					process.stdin.write(".quit\n")
					stdout, stderr = process.communicate()
			except IOError:
				continue
			except OSError as e:
				print "Folder " + e.filename +" not created"
				print "Exception : "+ e.strerror
		
	def getPlist(self):
		print "Decompressing plist files"
		mime = magic.Magic()
		for root, dirnames, filenames in os.walk(self.pathData):
		  for filename in fnmatch.filter(filenames, "*.plist"):
		  	try:
				  	if self.verbose:
				  		print "Plist file found : "+ root +"/"+ filename
				  	
				  	if not os.path.isdir(self.pathPlist + "/" + root.replace(self.pathData, "")):
				  		os.makedirs(self.pathPlist + "/" + root.replace(self.pathData, ""))
				  	
				  	cmd = "plistutil -i " + root + "/" + filename + " -o " + self.pathPlist + "/" + root.replace(self.pathData, "") + "/" + filename
				  	process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
				  	stdout, stderr = process.communicate()
			except IOError:
				continue
			except OSError as e:
				print "Folder " + e.filename +" not created"
				print "Exception : "+ e.strerror
	
	def getLogs(self):
		print "Getting logs"
		cmd = self.basesshcmd + "grep -Ei \"" + self.appname + "\[[0-9]{1,4}\]: \" /var/log/syslog"
		writeResultToFile(cmd, self.path + "/logs", self.verbose)
