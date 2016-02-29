#!/usr/local/bin/python2
#
# Author	Leroy van Logchem
# Created	Jan 2015
# Last mod	Nov 2015
# Description	Analyse unlimited amount of find output lines
#               Calculate sum per year
#
import pprint
import time
import sys
import re
from collections import defaultdict  # available in Python 2.5 and newer
from datetime import date

dict_projects	= defaultdict(lambda: defaultdict(int))
i		= 0
max_age		= 20 # years
max_age_year	= (date.today().year - max_age) + 1
year_now	= date.today().year
DEBUG		= False
DEBUGINPUT	= False
DEBUGDICT	= False
DEBUGAGE	= False

input = sys.stdin
for line in input:
	line		= line.strip()
	filename_array	= line.split('/',-1)
        pat		= re.compile(r'\s+')
	sizedate_str	= pat.sub(";",filename_array[0])
	sizedate_array  = sizedate_str.split(';') # Optimized using profiling, reduce amount of split calls
	bytesize	= int(sizedate_array[-5])
	fileyear	= int(sizedate_array[-2])
        if DEBUGINPUT:
		print line
	        pprint.pprint(sizedate_str)
	        pprint.pprint(filename_array)
		pprint.pprint(bytesize)
		pprint.pprint(fileyear)
	seconddir	= filename_array[2]
	projectname	= filename_array[3]

	# Focus on /tank/projects/someproject entries only
	if seconddir != 'projects': continue
	# Has the dictionary key been initialized before?
	if projectname not in dict_projects:
		# Init the years for csv output
		for year in range(max_age):
			dict_projects[projectname][year_now - year] = 0
		if DEBUGDICT:
			print '-' * 80
			print "Dictionary has been initialized"
			print '-' * 80
			pprint.pprint(dict_projects)
			print '-' * 80

	# OUTPUT is SIZE in BYTES
	if fileyear <= max_age_year:
		if DEBUGAGE:
			print "DEBUGDICT: Ancient file"
			print line
			pprint.pprint(dict_projects)
			print '-' * 80
		dict_projects[projectname][max_age_year] += bytesize
	elif fileyear > year_now:
		dict_projects[projectname][year_now] += bytesize
		if DEBUGAGE:
			print "DEBUGDICT: File from the future"
			print line
                        print year_now
			pprint.pprint(dict_projects)
			print '-' * 80
	else:
		dict_projects[projectname][fileyear] += bytesize

	# Stop parsing after how many records?
	#if i > 10**7: break

	del bytesize
	i += 1
input.close()

for key,value in dict_projects.iteritems():
	sys.stdout.write(key)
	for k2,v2 in value.iteritems():
		gb = int(v2/10**9)
		sys.stdout.write(',')
		# The output is using GB
		sys.stdout.write(str(gb))
		del gb
	sys.stdout.write("\n")
