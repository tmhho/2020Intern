import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import sys
import os
import numpy as np
import afstools

settings_filename = sys.argv[1]
settings = afstools.read_json(settings_filename)
sampling_type = settings["sampling type"]
mutation_rate = settings["theta"]
num_islands = settings["number of islands"]
omega = settings["omega"]
filename = settings["runtime filename"]
segsites = settings["number of segsites"]
data = pd.read_csv(filename)

fig = go.Figure()
M = np.logspace(start=-2, stop = 1, num = 3)
color = ['firebrick','royalblue','orange', 'purple']
for i in range(len(M)):
    fig.add_trace(go.Scatter(x=list(data['samples_size']),
                             y=list(data['ms_runtime_M{}'.format(M[i])]),
                             mode='lines+markers',
                             line=dict(color=color[i], 
                                width=2),
                             name='ms_runtime_M={}'.format(M[i])))
    fig.add_trace(go.Scatter(x=list(data['samples_size']),
                             y=list(data['qmd_runtime_M{}'.format(M[i])]),
                             mode='lines',
                             line=dict(color=color[i], width=2, dash='dash'),
                             name='qmd_runtime_M={}'.format(M[i])))

fig.update_layout(
    title=f'Performance, {segsites} segsites, {num_islands} islands, sampling_type {sampling_type}, theta = {mutation_rate}',
    xaxis_title='samples size',
    yaxis_title='runtime',
    yaxis_type='log' 
)
#fig.show()
if not os.path.exists('graphs'):
    os.mkdir('graphs')
path = os.path.join('graphs', settings["basename"] + 'visualization.png')
pio.write_image(fig , path, 'png')