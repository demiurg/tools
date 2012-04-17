#!/usr/bin/env python

import os, sys, glob, csv
import random
from random import choice
from dateutil import parser

create_format = "django"
model_name = "Birds"
tbl_name = "geohealth_birds"
files = glob.glob("./*.txt")

fields = []

for f in files:
    data = csv.DictReader(open(f, 'r'))
    fields.append(set(data.fieldnames))
    
fields = set.intersection(*fields)

query = "INSERT INTO %s (%s) VALUES ('%s');"
names = ", ".join(fields)
samples = []
lengths = {}

for f in fields:
    lengths[f] = 0
    
count = 0
for f in files:
    data = list(csv.DictReader(open(f, 'r')))
    random_rows = random.sample(xrange(len(data)), 3)
    for row_num, row in enumerate(data):
        values = []
        
        for field in fields:
            values.append(row[field])
            if len(row[field]) > lengths[field]:
                lengths[field] = len(row[field])
            
        if row_num in random_rows:
            samples.append(values)
        
        values = "', '".join(values)
        print query % (tbl_name, names, values)
        #print values
        count += 1

if create_format == "django":
    def guess(values, name):
        type = "models.TextField(null=True, blank=True)"
        val = values[0]
        try:
            int(val)
            type = "models.IntegerField(null=True, blank=True)"
        except ValueError:
            try:
                float(val)
                type = "models.FloatField(null=True, blank=True)"
            except ValueError:
                type = "models.CharField(max_length=%d, null=True, blank=True)" % (lengths[name])
                
        return type
        
    #print "Number of records: "+count
    create_tpl = "class %s(models.Model):%s"
    columns = "\n"
    field_num = 0
    for name in fields:
        vals = []
        for row in samples:
            vals.append(row[field_num])
        
        type = guess(vals, name)
        
        columns += "    %s = %s # %s\n" % (name, type, vals[0])
        
        field_num += 1
        
    print create_tpl % (model_name, columns)
    
elif create_format == "pgsql":
    def guess(values, name):
        type = "text"
        val = values[0]
        try:
            int(val)
            type = "integer"
        except ValueError:
            try:
                float(val)
                type = "double precision"
            except ValueError:
                type = "varchar(%d)" % (lengths[name])
                
        return type
        
    #print "Number of records: "+count
    create_tpl = "CREATE TABLE %s (%s);"
    columns = "\n"
    field_num = 0
    for name in fields:
        vals = []
        for row in samples:
            vals.append(row[field_num])
        
        type = guess(vals, name)
        
        columns += "\t%s\t%s,\t--- guess based on: %s\n" % (name, type, vals[0])
        
        field_num += 1
        
    print create_tpl % (tbl_name, columns)