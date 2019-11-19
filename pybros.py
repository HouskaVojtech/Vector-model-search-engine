#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import argv
from os import listdir
from os.path import isfile, join

from utilities import *

file_names = ['./documents/' + f for f in listdir('./documents')]
store_names( 'names', file_names )

document_list = read_all( file_names ) # array of word arrays - each document is one array of words

rated_terms = rate_terms( document_list ) # each word as [key], with occurrence as [value]

weights_of_terms = weight_terms( rated_terms, document_list )

labeled_matrix = label_occurences( weights_of_terms, uniq_terms( document_list ) )

if (len(argv) > 1 and argv[1] == '--linear'):
    invert_indexed__linear = invert_index__linear ( labeled_matrix )
    store_inverted( 'linear__data_storage', invert_indexed__linear )
else:
    invert_indexed = invert_index( labeled_matrix )
    store_inverted( 'data_storage', invert_indexed )

# revert_indexed = unlabel( revert_index( invert_indexed, len(document_list) ) )
