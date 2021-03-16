# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from Bio import Entrez
import os




def search(query):
    Entrez.email = 'vincent.breton@dataiku.com' # enter an authentic email ID to retrieve more data with uninterupted access
    handle = Entrez.esearch(db='pubmed', # database name is pubmed
                            sort='relevance', # sort by relevance or date
                            retmax='100000', # upper limit on the number of records to be retrieved
                            retmode='xml', # retrieval mode can be either xml or text
                            term=query,
                            verbose=3)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'vincent.breton@dataiku.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results



def build_pubmed_authors_request(row):
    """
    Build the request for an query based on an author.
    Sequence pattern: <FIRST_NAME> <LAST_NAME>[Author - Full]
    """
    return row['PDS prénom'] + ' ' + row['PDS nom'] + ' ' + '[Author - Full]'

cnt = 0

def fetch_papers(request):

    """Fetch Papers function"""

    global cnt

    results = search(request) # request ids publications
    id_list = results['IdList']

    cnt += 1
    print('Request #{} ({}), {} papers matched'.format(cnt, request, len(id_list)))

    if id_list: # if author published anything, we retrieve the papers based on this papers ids
        papers = fetch_details(id_list)
        author = request.split('[')[0].strip()
    else:
        papers = None
        author = None
    return papers, author

def fetch_author_from_paper(id):
    papers = fetch_details(id)
    len_authors = len(papers['PubmedArticle'][0]['MedlineCitation']['Article']['AuthorList'])
    authors = []
    for aut in range(len_authors):
        lastName = papers['PubmedArticle'][0]['MedlineCitation']['Article']['AuthorList'][aut]['LastName']
        foreName = papers['PubmedArticle'][0]['MedlineCitation']['Article']['AuthorList'][aut]['ForeName']
        author = foreName + ' ' + lastName
        authors.append(author)
    return authors