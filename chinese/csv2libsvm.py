#!/usr/bin/env python

"""
Convert CSV file to libsvm format. Works only with numeric variables.
Put -1 as label index (argv[3]) if there are no labels in your file.
Expecting no headers. If present, headers can be skipped with argv[4] == 1.

"""
#python csv2libsvm.py question_chinese.csv question_chinese1 0 1
#0 for class, 1 for headers

import sys
import csv
from collections import defaultdict

def construct_line( label, line ):
	new_line = []
	if float( label ) == 0.0:
		label = "0"
	new_line.append( label )

	for i, item in enumerate( line ):
		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%s:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line

# ---
print"python csv2libsvm.py question_chinese.csv question_chinese 0 1"
def output():
    input_file = "question_chinese.csv"
    output_file = "question_chinese1"
    label_index = 0
    skip_headers = 1
    classes = {}

    i = open( input_file, 'rb' )
    reader = csv.reader( i )
    headers = reader.next()
    for row in reader:
        if row[0] in classes:
            classes[row[0]]+=1
        else:
            classes[row[0]]=1
    o = open( output_file, 'wb' )
    print classes.items()

    for j in range(2):
        i = open( input_file, 'rb' )
        reader = csv.reader( i )
        if skip_headers:
            headers = reader.next()
        for line in reader:
            if label_index == -1:
                label = '1'
            else:
                label = line.pop( label_index )

            new_line = construct_line( label, line )
            for k in range(6/classes[label]):
                o.write( new_line )
        i.close()
    o.close()
