#!/usr/bin/python
import sys
import os

with open(sys.argv[1], 'r') as temp:
	msg = temp.read()
	msg = msg[:-1]
	if '#' in msg:
		start = msg.find('#')
		num = msg[start+1:]
		os.system('qbug close %s'%num)