#!/usr/bin/python
import time
import sys
import ConfigParser
import os
import os.path

class Bug(object):
	def __init__(self, file, ID=None, Desc=None):
		self.config = {}
		self.parser = ConfigParser.RawConfigParser()
		self.file = file
		if ID:
			with open('.bugs/' + file, 'w') as configfile:
				for section in self.parser.sections():
					for option in self.parser.options(section):
						self.config[section][option] = self.parser.get(section, option)
				self.parser.add_section('Bug')
				self.parser.set('Bug','ID',ID)
				self.parser.set('Bug','CREATED', time.ctime())
				self.parser.set('Bug','MODIFIED', time.ctime())
				self.parser.set('Bug','DESC', Desc)
				self.parser.set('Bug','COMPLETED', False)
				for section in self.parser.sections():
					self.config[section] = {}
					for option in self.parser.options(section):
						self.config[section][option] = self.parser.get(section, option)
				self.parser.write(configfile)
				
		if ID == None:
			with open('.bugs/' + file, 'r') as configfile:
				self.parser.readfp(configfile)
				for section in self.parser.sections():
					#print section
					self.config[section] = {}
					for option in self.parser.options(section):
						#print option
						self.config[section][option] = self.parser.get(section, option)
				self.parser.set('Bug','modified', time.ctime())

	def remark(self, note):
		if self.parser.has_option('Bug','remark'):
			existing = self.parser.get('Bug','remark')
		else:
			existing = ''
		note = existing + ' | ' + note
		self.parser.set('Bug','REMARK',note)
		with open('.bugs/' + self.file, 'w') as configfile:
			self.parser.write(configfile)
	
	def close(self):
		self.parser.set('Bug','COMPLETED', True)
		self.parser.set('Bug','MODIFIED', time.ctime())
		with open('.bugs/' + self.file, 'w') as configfile:
			self.parser.write(configfile)
		
def parse_opt():
	if len(sys.argv) > 1:
		if sys.argv[1] == 'add':
			new_bug()
		elif sys.argv[1] == 'remark':
			remark()
		elif sys.argv[1] == 'recall':
			if len(sys.argv) > 2:
				if sys.argv[2] == '-a':
					list(True)
				else:
					id = int(sys.argv[2])
					recall(id)
			else:
				list()	
		elif sys.argv[1] == 'close':
			close()
		
def new_bug():
	bugs = load_bugs()
	if not bugs:
		bugs = []
	desc = ''
	for string in sys.argv[2:]:
		desc = desc+ ' ' +string
	id = len(bugs) + 1
	newbug = Bug(str(id), ID=id, Desc=desc)
	recall(id)
	return newbug
	
def load_bugs():
	if os.path.isdir('.bugs'):
		x = 0
		bugs = []
		bugs2 = {}
		for bug in os.listdir('.bugs'):
			bugs.append(bug)
		bugs.sort()
		return bugs
	else:
		return False
			
def remark():
	bugs = load_bugs()
	id = int(sys.argv[2])
	if len(bugs) >= id-1:
		bug = bugs[id-1]
		note = ''
		for string in sys.argv[3:]:
			note = note + ' ' + string
		bug = Bug(bug)
		bug.remark(note)
	recall(id)
		
def recall(id):
	bugs = load_bugs()
	
	if len(bugs) >= id-1:
		bug = bugs[id-1]
		bug = Bug(bug)
		#print bug.config
		if bug.config['Bug']['completed'] == 'True':
			completed = 'X'
		else:
			completed = ' '
			
		print '[%s] ID:%s - %s'%(completed, bug.config['Bug']['id'], bug.config['Bug']['desc'])
		print '    CREATED : %s'%(bug.config['Bug']['created'])
		print '    MODIFIED: %s'%(bug.config['Bug']['modified'])
		if 'remark' in bug.config['Bug']:
			print '    REMARK: %s'%(bug.config['Bug']['remark'])
			
def list(all = False):
	bugs = load_bugs()
	if bugs:
		for bug in bugs:
			if all:
				recall(int(bug))
			else:
				bug = Bug(bug)
				if bug.config['Bug']['completed'] == 'True':
					completed = 'X'
				else:
					completed = ' '
					
				print '[%s] ID:%s - %s'%(completed, bug.config['Bug']['id'], bug.config['Bug']['desc'])
		
def close():
	bugs = load_bugs()
	id = int(sys.argv[2])
	if len(bugs) >= id-1:
		bug = bugs[id-1]
		bug = Bug(bug)
		bug.close()
			
parse_opt()
		
