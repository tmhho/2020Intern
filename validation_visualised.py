import pandas as pd
import glob
import plotly.graph_objects as go
import plotly.io as pio
import os
import sys
import numpy as np

total_sample = sys.argv[1]
sampling_scheme = sys.argv[2]

filename = os.path.join('csv-files',f'*_errors_k={total_sample}_10i_sampling={sampling_scheme}_omega=1.25_theta=0.1.csv')
file = glob.glob(filename)
versions= list(range(1,4))
M = np.logspace(start=-2, stop = 1, num = 10)
M=[M[0], M[5], M[9]]
data = pd.read_csv(file[0])


#####################DRAWING GRAPH##############################
fig = go.Figure()

color = ['firebrick','royalblue','green']

for i in range(len(M)):
	for ver in versions: 
		fig.add_trace(go.Scatter(
		x=list(data['num_segsites']),
		y = list(data[f'ver{ver}_average.abs.error_M{M[i]}']),
		mode='lines+markers',
		opacity = 0.4,
		line=dict(color=color[i]),
		name = f'M = {M[i]} - ver {ver}'))
   
fig.update_layout(
	title='Validation: nislands=10 k={} sampling_vector = {}'.format(total_sample,sampling_scheme),
	xaxis_title='num_segsites',
	yaxis_title='average_abs_error', 
	xaxis_type='log',
	yaxis_type='log')
# fig.show()

###############SAVE FIGURE######################################
if not os.path.exists('graphs'):
	os.mkdir('graphs')
if not os.path.exists('html-files'):
	os.mkdir('html-files')
path_png = os.path.join ('graphs', 'Validation_'+ file[0][10:-4] + '.png')
path_html = os.path.join('html-files','Validation_'+ file[0][10:-4] + '.html')
pio.write_image(fig, path_png, format='png')
fig.write_html(path_html)