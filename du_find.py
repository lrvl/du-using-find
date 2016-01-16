#!/usr/bin/env python2.7
import sys
import re
import pprint
from collections import defaultdict  # available in Python 2.5 and newer

dict_dirs       = defaultdict(lambda: defaultdict(int))
DEBUG		= 0

def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)

input = sys.stdin
for line in input:
        line            = line.strip()
        line_array      = line.split('/',-1)
        re_pat          = re.compile(r'\s+')			# Match one or more whitespace characters
        leftside_str    = re_pat.sub(";",line_array[0])
        del line_array[0]

        sizedate_array  = leftside_str.split(';')		# Optimized using profiling, reduce amount of split calls
        bytesize        = int(sizedate_array[-5])
        if DEBUG:
                print line
                pprint.pprint(leftside_str)
                pprint.pprint(line_array)
                pprint.pprint(bytesize)


	for index,dirname in enumerate(line_array):
		dirname_str = '/'.join(map(str,line_array[0:index]))
                if dirname_str == "":
			continue
		if dirname_str not in dict_dirs:
                        dict_dirs[dirname_str] = 0
		if bytesize < 512:				# At least account 512 bytes
			dict_dirs[dirname_str]+=512
		else:
			dict_dirs[dirname_str]+=bytesize

for dirname in sorted(dict_dirs, key=dict_dirs.get, reverse=True):
	try:
		print "%i\t%s" % (dict_dirs[dirname],dirname)
		sys.stdout.flush()
	except IOError:
	    # stdout is closed, no point in continuing
	    # Attempt to close them explicitly to prevent cleanup problems:
		try:
			sys.stdout.close()
		except IOError:
			pass
		try:
			sys.stderr.close()
		except IOError:
			pass
