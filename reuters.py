#!/usr/bin/python3
# -*- coding: utf-8 -*-

from nltk.corpus import reuters

documents = reuters.fileids()

categories = reuters.categories();

# print(categories);

cnt = 0
for cat in categories:
  n = 0
  category_docs = reuters.fileids(cat)
  for doc_id in category_docs:
    doc = open( './documents/' + cat + str( cnt ), "w")
    doc.write( reuters.raw ( doc_id ) )
    doc.close()
    cnt += 1
    n += 1
    if n == 50:
      break
