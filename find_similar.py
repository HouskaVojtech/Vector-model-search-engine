#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import argv
from os import listdir
from os.path import isfile, join
from utilities import *

# file_names = ['./documents/' + f for f in listdir('./documents')]

file_names = load_names( 'names' )


if (len(argv) > 2 and argv[2] == '--linear'):
  storage = 'linear__data_storage'
else:
  storage = 'data_storage'

loaded = load_inverted( storage )

listified = listify( loaded )

distances = cos_simil(file_names.index('./documents/' + argv[1]), listified)

srtd = list( map( lambda record: (file_names[record[0]], record[1]),
  list( sorted( distances, reverse = True, key = lambda item: value( item ) ) ) ) )

for line in srtd:
  print( line )

# revert_indexed =  revert_index( loaded, len( file_names ) )
