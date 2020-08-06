import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import glob
import sys
import os
import numpy as np
# filenames = glob.glob('afs_runtimes_n*')
# M = [float(name.split('_')[2].split('=')[1]) for name in filenames]

# filenames = ['afs_distances_M=0.1_10i.csv','afs_distances_M=1_10i.csv','afs_distances_M=10_10i.csv']

# combined_csv = pd.concat( [ pd.read_csv(f) for f in filenames ], sort=False )
# combined_csv.to_csv( "runtime_Mvar.csv", index=False )
# pd.read_csv("runtime_Mvar.csv", header=None).T.to_csv( "transposed.runtime_Mvar.csv", header=False, index=False)
# data = pd.read_csv("transposed.runtime_Mvar.csv")
# data = []
# for file in filenames :
#     data.append([pd.read_csv(file)])

sampling_type = sys.argv[1]
mutation_rate = 1.0
num_islands = 10
omega = 1.25
theta =1.0 
filename = os.path.join('csv-files',f'*_runtimes_{num_islands}i_sampling={sampling_type}_omega={omega}_theta={mutation_rate}.csv')
file = glob.glob(filename)[0]
data = pd.read_csv(file)

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
    title=f'Performance, nsegsites = 500 000, 10 islands, sampling_type = {sampling_type}, theta = {mutation_rate}',
    xaxis_title='samples size',
    yaxis_title='runtime',
    yaxis_type='log' 
)
#fig.show()
if not os.path.exists('graphs'):
    os.mkdir('graphs')
path = os.path.join(f'graphs', f'Performance_'+ file[10:-4] +'.png')
pio.write_image(fig , path, 'png')