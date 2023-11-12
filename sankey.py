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


# publications
# ------------
pubs = ['c: IEEE MED',
        'c: IEEE SYSCON',
        'c: IEEE ICUAS',
        'c: IEEE SYSCON',
        'c: IEEE CCECE',
        'c: IEEE ICUAS',
        'c: IFAC WC',
        'c: IFAC WC',
        'j: IEEE Sys J',
        'j: IEEE Sys J',
        'c: IEEE SYSCON',
        'j: IEEE Potentials',
        'j: Int J Adapt Cont Sig Proc',
        'c: IEEE SYSCON',
        'c: IFAC WC',
        'c: IFAC WC',
        'j: IEEE Sys J',
        'c: IEEE SYSCON',
        'j: J Intel Rob Sys',
        'j: IEEE ACCESS',
        'j: IEEE Trans Net Sci Eng',
        'j: J Intel Rob Sys',
        'c: IEEE SYSCON'
        ]

# disciplines
# -----------
discs = ["Swarming", "Control", "Learning"]

# labels
# ------
labels = discs + pubs 

# publication dates
# -----------------
dates = [2015,
        2016,
        2017,
        2017,
        2017,
        2017,
        2017,
        2017,
        2017,
        2018,
        2018,
        2018,
        2019,
        2019,
        2020,
        2020,
        2020,
        2020,
        2021,
        2022,
        2023,
        2023,
        2023
        ]
dates_norm = [(x - 2015+2)/(2023-2015+2) - 0.1 for x in dates]

# connect pubs to disciplines
# -----------------------------
connects = [1,
        1,
        1,
        [1,2],
        2,
        2,
        [0,1],
        [1,2],
        [1,2],
        [1,2],
        1,
        [1,2],
        [1,2],
        0,
        [0,1],
        0,
        [1,2],
        [0,1],
        [0,1,2],
        [0,1],
        [0,1],
        0,
        0]

# draw the connections
# -------------------
connects_target = []
connects_source = []
xs = dates_norm
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
        for j in connects[i]:
        
            connects_target += [i+len(discs)]
            connects_source += [j]
            
            if j == 0:
                color_links += ['rgba(255, 192, 192 0.5)']
            elif j == 1:
                color_links += ['rgba(192, 192, 255 0.5)'] 
            elif j == 2:
                color_links += ['rgba(192, 255, 192 0.5)']


# align by publcation dates
# ------------------------
ys = [0.3, 0.2, 0.1] + xs 
xs = [0, 0, 0] + xs 

# draw the nodes
# --------------
color_node = []

for k in pubs:
    
    if k[0] == 'c':
        color_node += ['rgba(255, 255, 255, 0.2)']
    elif k[0] == 'j':
        color_node += ['rgba(0, 0, 0, 0.2)']

color_node = ['rgb(255, 192, 192, 0.8)', 'rgb(192, 192, 255,0.8) ', 'rgb(192, 255, 192,0.8)'] + color_node

# add degrees
# ------------
degrees = ['Phd (Queen\'s)']
degrees_year_norm = [(x - 2015+2)/(2023-2015+2) for x in [2018.5]]
degrees_source = [5,6,7,8,9,10,11,12,13,14]
degrees_target = [26,26,26,26,26,26,26,26,26,26]
degrees_color = ['rgba(180, 128, 200, 0.5)']
degrees_color_links = []
for i in degrees_source:
    degrees_color_links += ['rgba(180, 128, 200, 0.5)']

# produce the chart
# -----------------
fig = go.Figure(go.Sankey(
    arrangement = "snap",
    node = {
        "label": labels + degrees,
        "x": xs + degrees_year_norm,
        "y": ys + [0.2],
        'pad':1,
        'color': color_node + degrees_color,
        },  # 10 Pixels
    link = {
        "source": connects_source + degrees_source,
        "target": connects_target + degrees_target,
        'color': color_links + degrees_color_links,
        "value": list(np.ones(len(connects_source + degrees_source)))
        }))


fig.update_layout(
    font_size=15
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