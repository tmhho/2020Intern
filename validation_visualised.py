import pandas as pd
import glob
import plotly.graph_objects as go
import plotly.io as pio
import os
import sys

# filenames = glob.glob('afs_errors_k=8_10i_sampling={}')
# filenames.sort()
total_sample = sys.argv[1]
sampling_scheme = sys.argv[2]

filename = os.path.join('csv-files','afs_errors_k={}_10i_sampling={}.csv'.format(total_sample,sampling_scheme))
M = [0.1, 1.0, 10.0]
data = pd.read_csv(filename)


#####################DRAWING GRAPH##############################
fig = go.Figure()

#color = ['firebrick','royalblue','yellow','green']

for i in range(len(M)):
	fig.add_trace(go.Scatter(
		x=list(data['repetitions']),
		y = list(data['abs.error_{}'.format(M[i])]),
		mode='lines+markers',
		name='abs.error_{}'.format(M[i])))
   
fig.update_layout(
	title='Validation: nislands = 10, k={}, sampling_vector = {}'.format(total_sample,sampling_scheme),
	xaxis_title='nreps',
	yaxis_title='abs_error', 
	xaxis_type='log')
# fig.show()

###############SAVE FIGURE######################################
if not os.path.exists('graphs'):
	os.mkdir('graphs')
path = os.path.join ('graphs', 'Validation:nislands=10_k={}_sampling_vector={}.png'.format(total_sample,sampling_scheme))
pio.write_image(fig, path, format='png')