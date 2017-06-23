#!/usr/bin/python
import json
from pprint import pprint

with open('htsdata2017.json') as data_file:    
    data = json.load(data_file)

for key in data:
    if str(key['htsno']).startswith('3924.10'):
        pprint(key)
