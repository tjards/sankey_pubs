#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:39:30 2023

This program produces a sankey chart for publication record by discipline

Note: link this to Google Scholar to autogenerate 

@author: tjards
"""

# import stuff
# ------------
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default='browser'
import my_scholar as schol

# pull data from Google Scholar
# ----------------------------
my_name = 'Peter Travis Jardine'
pubs, dates, dates_norm, titles, discs, connects = schol.build_lists(my_name)
print('processing...')

# manually add degree information
# ------------------------------
degree = ['Phd (Queen\'s)']    # only accepts one degree right now
degree_start = 2015             # start year (to count pubs)
degree_stop = 2018.5            # end year (to count pubs)

# labels
# ------
labels = discs + pubs 

# draw the connections
# -------------------
connects_target = []
connects_source = []
xs = [x for x in dates_norm]
ys = [0.9*x for x in xs]
color_links = []

for i in range(0,len(connects)):
    
    if type(connects[i]) == int:
        
        connects_target += [i+len(discs)]
        connects_source += [connects[i]]
        if connects[i] == 0:
            color_links += ['rgba(255, 192, 192, 0.5)']
        elif connects[i] == 1:
            color_links += ['rgba(192, 192, 255 0.5)'] 
        elif connects[i] == 2:
            color_links += ['rgba(192, 255, 192, 0.5)']
        else:
            color_links += ['rgba(0, 0, 0, 0.2)']
             
    else:
        for j in connects[i]:
        
            connects_target += [i+len(discs)]
            connects_source += [j]
            
            if j == 0:
                color_links += ['rgba(255, 192, 192 0.5)']
            elif j == 1:
                color_links += ['rgba(192, 192, 255 0.5)'] 
            elif j == 2:
                color_links += ['rgba(192, 255, 192 0.5)']
            else:
                color_links += ['rgba(0, 0, 0, 0.2)']


# align by publcation dates
# ------------------------
discsx      = []
discsy      = []
left_edge   = 0
for s in range(0,len(discs)):
    discsy = discsy + [0.1*s + 0.1]
    discsx = discsx + [0]
ys = discsy + ys 
xs = discsx + xs   
    
# add degrees
# ------------
degrees_source = []
degrees_target = []
degrees_year_norm = [(x - min(dates) + 1)/(max(dates)-min(dates) + 1) for x in [degree_stop]]
# look through pubs
for d in range(0,len(pubs)):
    # if publication occured during degree
    if dates[d] > degree_start and dates[d] < degree_stop:
        degrees_source = degrees_source + [len(discs) + d]
        degrees_target = degrees_target + [len(discs) + len(pubs)]

# add colors
degrees_color = ['rgba(255, 255, 255, 0.2)']
degrees_color_links = []
for i in degrees_source:
    degrees_color_links += ['rgba(180, 128, 200, 0.5)']


# draw the nodes
# --------------
color_node = []

# make the pubs white
for k in pubs:
    color_node += ['rgba(255, 255, 255, 0.2)']
color_node = ['rgb(255, 192, 192, 0.8)', 'rgb(192, 192, 255,0.8) ', 'rgb(192, 255, 192,0.8)'] + ['rgb(192, 255, 192,0.8)'] + color_node


# truncate labels
# ---------------
trunc_size = 10 # max length
# remove numbers
translation_table = str.maketrans("", "", "0123456789 ")
labels = [label.translate(translation_table) for label in labels]
# truncate
for i in range(len(discs),len(labels)):
    labels[i] = labels[i][0:trunc_size]

# produce the chart
# -----------------
fig = go.Figure(go.Sankey(
    arrangement = "snap",
    node = {
        "label": labels + degree,
        "x": xs + degrees_year_norm,
        "y": ys + [0.2],
        'pad':0.1,
        'color': color_node + degrees_color,
        },  # 10 Pixels
    link = {
        "source": connects_source + degrees_source,
        "target": connects_target + degrees_target,
        'color': color_links + degrees_color_links,
        "value": list(np.ones(len(connects_source + degrees_source)))
        }))


fig.update_layout(
    font_size=14
    )

for x_coordinate, column_name in enumerate(dates):
  fig.add_annotation(
          x=xs[x_coordinate+len(discs)],
          y = 1.05,
          xref="paper",
          yref="paper",
          text=column_name,
          showarrow=False,
          font=dict(
              size=16,
              color="black"
              ),
          align="center"
          )



fig.show()