import plotly.graph_objects as go
import pandas as pd
import glob
import sys
import os
import plotly.io as pio
import numpy as np
import afstools 


settings_filename = sys.argv[1]
settings_filename = os.path.join('csv-files',settings_filename)
settings = afstools.read_json(settings_filename)
total_samples = settings["total samples"]
sampling_scheme = settings["sampling type"]
islands = settings['number of islands']
migration_rates = settings["migration rates"]

data = pd.read_csv(settings["raw data filename"])

list_c=[]

for i in range(0,total_samples-1):
    c = [data['expected_afs_M{}'.format(M)][i] for M in migration_rates]
    list_c.append(c)
fig = go.Figure()
for i in range(len(list_c)):
        fig.add_trace(go.Scatter(
    x=migration_rates, y=list_c[i],
    hoverinfo='x+y',
    mode='lines+markers',
    line=dict(width=0.5
        # , color='rgb(131, 90, 241)'
        ),
    marker=dict( opacity=0.3),
    stackgroup='one',
    name = 'c{}'.format(i+1)# define stack group
))


fig.update_layout(title=f'Afs, k={total_samples}, nislands={islands}, sampling_scheme={sampling_scheme}'.format(total_samples,sampling_scheme), xaxis_type='log', xaxis_title='M')
if not os.path.exists('graphs'):
    os.mkdir('graphs')
path_png = os.path.join('graphs',settings['basename']+ 'area_chart.png')
pio.write_image(fig , path_png, 'png')

# fig.show()
