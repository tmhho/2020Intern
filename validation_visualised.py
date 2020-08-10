import afstools

import pandas as pd
import glob
import plotly.graph_objects as go
import plotly.io as pio
import os
import sys
import numpy as np

settings_filename = sys.argv[1]
settings = afstools.read_json(settings_filename)

total_samples = settings['total samples']
sampling_scheme = settings['sampling type']
versions = settings['iterations']
M = settings['migration rates']
data = pd.read_csv(settings['distances filename'])

##################### DRAWING GRAPH ##############################

fig = go.Figure()
color = ['firebrick', 'royalblue', 'green']
for i in range(len(M)):
	for ver in versions: 
		fig.add_trace(go.Scatter(
			x = list(data['num_segsites']),
			y = list(data[f'ver{ver}_average.abs.error_M{M[i]}']),
			mode = 'lines+markers',
			opacity = 0.4,
			line = dict(color=color[i]),
			name = f'M = {M[i]} - ver {ver}'
		))

fig.update_layout(
	title=f'Validation: islands=10; k={total_samples}; sampling = {sampling_scheme}',
	xaxis_title='segsites',
	yaxis_title='average absolute error', 
	xaxis_type='log',
	yaxis_type='log'
)

############### SAVE FIGURE ######################################

if not os.path.exists('graphs'):
	os.mkdir('graphs')

if not os.path.exists('html-files'):
	os.mkdir('html-files')

path_png = os.path.join ('graphs', settings['basename'] + 'visualization.png')
path_html = os.path.join('html-files', settings['basename'] + 'visualization.html')
pio.write_image(fig, path_png, format='png')
fig.write_html(path_html)