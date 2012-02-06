import os, sys, glob, csv

files = glob.glob("./*.txt")

fields = []

for f in files:
    data = csv.DictReader(open(f, 'r'))
    fields.append(set(data.fieldnames))

i = set.intersection(*fields)

data = csv
for f in files:
    data = csv.DictReader(open(f, 'r'))
    fields.append(set(data.fieldnames))