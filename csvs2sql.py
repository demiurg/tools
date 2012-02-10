#!/usr/bin/python

import os, sys, glob, csv

files = glob.glob("./*.txt")

fields = []

for f in files:
    data = csv.DictReader(open(f, 'r'))
    fields.append(set(data.fieldnames))
    
fields = set.intersection(*fields)

query = "INSERT INTO geohealth_birds (%s) VALUES ('%s');"
names = ", ".join(fields)

count = 0
for f in files:
    data = csv.DictReader(open(f, 'r'))
    for row in data:
        values = []
        
        for field in fields:
            values.append(row[field])
            
        values = "', '".join(values)
        print query % (names, values)
        #print values
        count += 1
        
#print "Number of records: "+count 
