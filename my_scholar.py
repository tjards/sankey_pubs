#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:52:58 2023

@author: tjards
"""

#%% import stuff
# ------------
from scholarly import scholarly
#source: https://github.com/scholarly-python-package/scholarly

#%% parameters
# ----------

#author_name = 'Peter Travis Jardine'
discs = ['control', 'learning', 'swarming']
degrees = ['Phd (Queen\'s)']

# this list will attempt to align keywords with disciplines (will search pub/title)
keywords_disciplines = [
    ['control', 'mpc', 'controller', 'regulator', 'pid', 'gain', 'systems'],
    ['machine learning', 'data', 'reinforcement', 'neural', 'ai', 'learning'],
    ['multi', 'agent', 'swarm', 'flock', 'swarming', 'swarms', 'cooperative']
    ]

#%% pull data
# -----------

def pull_data(author_name):

    # produce an iterator for author
    search_query = scholarly.search_author(author_name)

    # retrieve data on first result
    author = scholarly.fill(next(search_query))
    print('pulled data for ', author_name)
    
    return author

#%% Build lists
# -------------

def build_lists(author_name):

    author = pull_data(author_name)    
        
    # initialize lists 
    pubs = []
    dates = []
    titles = []
    connects = []
    
    # iterate through
    for i in range(0,len(author['publications'])):
        
        if not [author['publications'][i]['bib']['citation'].lower()]:
            pubs += ['unknown']
        else:
            pubs += [author['publications'][i]['bib']['citation'].lower()]
        
        if not [author['publications'][i]['bib']['title'].lower()]:
            titles += ['unknown']
        else:
            titles += [author['publications'][i]['bib']['title'].lower()]
        
        if not [int(author['publications'][i]['bib']['pub_year'])]:
            dates += [0]
        else:
            dates += [int(author['publications'][i]['bib']['pub_year'])]

        # initialize
        sublist = []
        disc_index = -1 
        # for each discipline
        for j in discs:
            disc_index += 1
            # search through keywords
            for k in keywords_disciplines[disc_index]:
                # check the publication name
                if k in author['publications'][i]['bib']['citation'].lower():
                    sublist = sublist + [disc_index]
                # check the title name
                if k in author['publications'][i]['bib']['title'].lower():
                    sublist = sublist + [disc_index]
        # if it's empty
        if not sublist:
            connects = connects + [list(set(sublist)) + [len(discs)]]
        else:
            connects = connects + [list(set(sublist))]
     
    # normalize the dates 
    date_min = min(dates)
    date_max = max(dates)
    dates_norm = [(x - date_min + 1)/(date_max-date_min + 1) for x in dates]

    return pubs, dates, dates_norm, titles, discs + ['other'], connects