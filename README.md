# iOSForensic

iosForensic is a python tool to help in forensics analysis on iOS.
It get files, logs, extract sqlite3 databases and uncompress .plist files in xml.


## Installation
Simply clone this git repository and install dependencies.

### Dependencies

#### Linux
- 	OpenSSH
- 	sshpass
-	sqlite3
-	python >= 2.6
-	[Python-magic](https://github.com/ahupp/python-magic/)
- 	[plistutil](http://cgit.sukimashita.com/libplist.git)

#### Device
-	a jailbroken device
- 	OpenSSH
- 	syslogd to /var/log/syslog (it's the name of the application, restart your phone after install)
- 	wifi ON
- 	on some firmware, usb connection needed

## How to use

### Options
-	-h --help : show help message
-	-a --about : show informations
-	-v --verbose : verbose mode
-	-i --ip : local ip address of the iOS terminal
-	-p --port : ssh port of the iOS terminal (default 22)
-	-P --password : root password of the iOS terminal (default alpine)
	
## Examples
	./iOSForensic.py -i 192.168.1.10 [OPTIONS] APP_NAME.app INCOMPLETE_APP_NAME APP_NAME2_WITHOUT_DOT_APP
	./iOSForensic.py -i 192.168.1.10 -p 1337 -P pwd MyApp.app angry MyApp2

## Author
Written by Florian Pradines (Phonesec), this tool is a referenced OWASP iOS security project since june 2014.

You can contact me via my [website](http://florianpradines.com)

## Licence
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
