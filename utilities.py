import re
import copy
from functools import reduce
from math import sqrt, pow
import itertools

import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

ps = PorterStemmer ()


# def termCntIn ( doc , term ):
#     cnt = 0
#     for one in doc:
#         if term == one:
#             cnt += 1
#     return cnt

def read_words ( file ):
    container = []

    for line in file.readlines():
        for raw_word in line.split():
            clean_word = re.sub( '[^a-z]', '', raw_word.lower() ) 
            if clean_word != '':
                container.append ( clean_word )

    return container

def filter_stop_w ( words ):
    filtered = []
    stopWords = set ( stopwords.words( 'english' ) )

    for word in words: 
        if word not in stopWords:
            filtered.append (word)

    return filtered

def read_document ( filename ): 
    result = []

    file = open( filename,"r" )
    words = read_words( file )
    filtered = filter_stop_w( words )
    
    for word in filtered:
        result.append( ps.stem( word ) )

    return result


def read_all ( document_names ):
    words_in_docs = []

    for file_name in document_names:
        words_in_docs.append( read_document ( file_name ) )

    return words_in_docs

def rate_terms ( terms_arr ):
    terms = {} #number of occurrences for each term in each document

    for document in terms_arr:
        for term in document:
            if term in terms:
                terms [term] += 1
            else:
                terms [term] = 1

    return terms

def count_words_in ( documents ):
    words_in_docs = []

    for document in documents:
        words_in_docs.append( len( document ) )

    return words_in_docs

def clone_n_clear ( original ):
    clone = copy.deepcopy( original )

    for key in clone.keys():
        clone[key] = 0

    return clone

def label_occurences ( matrix, terms ):
    return dict( zip( terms, matrix ) ).items()

def index_item__linear ( item ):
    return (item[0],
        list( map( lambda pair: tuple( reversed( pair ) ),
            list( enumerate( item[1] ) ) ) )
    )

def index_item ( item ):
    return (item[0],
        list( map( lambda pair: tuple( reversed( pair ) ),
            list( filter( lambda pair: pair[1], list( enumerate( item[1] ) ) ) ) ) )
    )

def invert_index__linear ( labeled ):
    return [ index_item__linear(item) for item in labeled ]

def invert_index ( labeled ):
    return [ index_item(item) for item in labeled ]

def patch_item ( default, patch ):
    for record in patch:
        default[record[1]] = record[0]

    return default

def revert_index ( invert_indexed, doc_cnt ):
    return [(item[0], patch_item( [0 for _ in range( doc_cnt )], item[1] )) for item in invert_indexed ]

def unlabel( revert_indexed ):
    return list( map( lambda pair: pair[1], revert_indexed ) )

def create_doc_list ( doc, terms_dic ): # vytvor list vyskytu slov v dokumentu
    terms_rate = copy.deepcopy( terms_dic )
    for word in doc:
        terms_rate[word] += 1

    return list( terms_rate.values() )

def get_term ( record ):
    return record[0]

def get_occurrences ( record ):
    return record[1]

def tuple_tostr ( tuple ):
    return reduce( lambda acc, val : ' '.join( [ acc, str( val ) ] ), tuple, '' ).strip()

def tuple_list_tostr ( lst ):
    return reduce ( lambda acc, val: ' '.join( [ acc, tuple_tostr( val ) ]), lst, '')

def store_inverted ( filename, invert_indexed ):
    with open( filename, 'w' ) as file:
        for record in invert_indexed:
            weights = tuple_list_tostr( get_occurrences( record ) )
            file.write( ''.join( [ get_term( record ), weights, '\n' ] ) )

def to_pairs ( lst ):
    return list( map( 
        lambda pair: ( float( pair[0] ), int( pair[1] ) ), list( zip( * [ iter( lst ) ] * 2 ) ) ) )

def load_record ( line ):
    return ( line[0], to_pairs( line[1:] ) )

def load_inverted ( filename ):
    inverted = []

    with open( filename, 'r' ) as file:
        for line in file.readlines():
            inverted.append( load_record( line.split() ) )

    return inverted

def store_names ( filename, arr ):
    with open( filename, 'w' ) as file:
        for name in arr:
            file.write( name + '\n' )

def load_names ( filename ):
    names = []

    with open( filename, 'r' ) as file:
        for line in file.readlines():
            names.append( line.strip() )

    return names

def split_to ( lst ):
  first = [p[0] for p in lst ]
  second = [p[1] for p in lst ]

  return first, second

def treefy_indexed ( lst ):
  keys, values = split_to( list( map( lambda occ: list( reversed( occ ) ), lst ) ) )
  return dict( zip( keys, values ) )

def to_dict ( inverted ):
  indexed = {}

  for record in inverted:
    indexed[ get_term( record ) ] = treefy_indexed( get_occurrences( record ) )

  return indexed

def listify ( inverted ):
  return list( map( lambda record: treefy_indexed( get_occurrences( record ) ), inverted ) )

def first ( pair ):
  return pair[0]

def second ( pair ):
  return pair[1]

def index ( pair ):
  return first( pair )

def value ( pair ):
  return second( pair )

def simil ( x, y, index_vec_size ):
  return ( index( x ), value( x ) / sqrt( value( y )  * index_vec_size ) )

def cos_simil ( index, indexed ):
  numerator = {}
  denom = {}
  similarity = {}

  for record in indexed:
    if ( index in record ):
      lst = list ( map ( lambda items: (items[0] , record[index] * items[1] ), record.items() ) )
      for scalar in lst:
        numerator[scalar[0]] = numerator.get(scalar[0], 0) + scalar[1]
        denom[scalar[0]] = denom.get(scalar[0], 0) + (record[index] ** 2)

  index_vec_size =  denom[ index ]

  return list( map( lambda numer, denom: 
    simil(numer, denom, index_vec_size) , numerator.items(), denom.items() ) )

def inc_in ( dct, term ):
    dct[term] = dct.get(term, 0) + 1
    return dct

def tf_doc ( document, uniq_words ):
    return list( map( lambda term: reduce(
        lambda acc, i: acc + 1 if i == term else acc, document, 0. ) / len( document ), uniq_words))

def uniq_terms ( document_list ):
    return list( set( list( itertools.chain.from_iterable( document_list ) ) ) )

def weight_terms ( rated_terms, document_list ):
    # uniq_words = []
    # for document in document_list:
    #     for word in document:
    #         if word not in uniq_words:
    #             uniq_words.append( word ) 

    word_count = count_words_in( document_list ) # number of words in each document
    terms_rates = clone_n_clear( rated_terms ) # each word as [key] := 0
    matrix_tf = [] # matrix tf for each document

    uniq = uniq_terms( document_list )
    tf_matrix = list( map( lambda document: tf_doc( document, uniq ) , document_list ) )

    np_tf = np.array( tf_matrix, ndmin = 2, dtype = float )

    idf_vector = np.zeros( len( np_tf[0] ) )

    x = 0
    # np_matrix_tf ma shape DOCS x TERMS
    # chceme prochazet sloupce tak je treba ji transponovat
    for terms in np_tf.T: # pocet dokumentu obsahujici term
        for terms_in_doc in terms:
            if terms_in_doc != 0:
                idf_vector[x] += 1
        x += 1

    #np_matrix_tf is of shape DOCS x TERMS
    #np_matrix_tf je pocet termu v danym dokumentu
    doc_cnt = len( document_list ) #pocet dokumentu


    idf_vector = np.array ( np.log10( doc_cnt / idf_vector ), ndmin=2 )

    tf_idf = []

    for column, multip in list( zip( np_tf.T, idf_vector.T)):
        tf_idf.append( column * multip )

    return tf_idf