import pandas as pd
import glob
import plotly.graph_objects as go
import plotly.io as pio
import os
import sys
import numpy as np
# filenames = glob.glob('afs_errors_k=8_10i_sampling={}')
# filenames.sort()
total_sample = sys.argv[1]
sampling_scheme = sys.argv[2]

filename = os.path.join('csv-files','afs_errors_k={}_10i_sampling={}_omega=1.25_theta=0.1.csv'.format(total_sample,sampling_scheme))
# M = [0.05, 1.0, 10.0]
M = np.linspace(start=0.05, stop = 100.0, num = 25)
M = [M[0], M[1], M[12], M[24]]
data = pd.read_csv(filename)


#####################DRAWING GRAPH##############################
fig = go.Figure()

#color = ['firebrick','royalblue','yellow','green']

for i in range(len(M)):
	fig.add_trace(go.Scatter(
		x=list(data['num_segsites']),
		y = list(data[f'average.abs.error_{M[i]}']),
		mode='lines+markers',
		name=f'average_abs.error_{M[i]}'))
   
fig.update_layout(
	title='Validation: nislands=10 k={} sampling_vector = {}'.format(total_sample,sampling_scheme),
	xaxis_title='num_segsites',
	yaxis_title='abs_error', 
	xaxis_type='log',
	yaxis_type='log')
# fig.show()

###############SAVE FIGURE######################################
if not os.path.exists('graphs'):
	os.mkdir('graphs')
path = os.path.join ('graphs', 'Validation_nislands=10_k={}_sampling_vector={}_omega=1.25_theta=0.1.png'.format(total_sample,sampling_scheme))
pio.write_image(fig, path, format='png')