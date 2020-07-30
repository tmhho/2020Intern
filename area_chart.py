import plotly.graph_objects as go
import pandas as pd
import glob
import sys
import plotly.io as pio
import os
import numpy as np

total_samples = int(sys.argv[1])
sampling_scheme = sys.argv[2]
filename = os.path.join('csv-files','afs_values_k={}_10i_sampling={}.csv'.format(total_samples,sampling_scheme))

# list_M = [0.1, 1.0, 10.0]
list_M = np.linspace(start=0.05, stop = 100.0, num = 25)
data = pd.read_csv(filename)

list_c=[]
for i in range(0,total_samples-1):
    c = [data['expected_afs_M{}'.format(M)][i] for M in list_M]
    list_c.append(c)
fig = go.Figure()
for i in range(len(list_c)):
        fig.add_trace(go.Scatter(
    x=list_M, y=list_c[i],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5
        # , color='rgb(131, 90, 241)'
        ),
    stackgroup='one',
    name = 'c{}'.format(i+1)# define stack group
))


fig.update_layout(title='Afs, k={}, nislands=10, sampling_scheme={}'.format(total_samples,sampling_scheme), xaxis_type='log', xaxis_title='M')
if not os.path.exists('graphs'):
    os.mkdir('graphs')
path = os.path.join('graphs', 'Area_Chart_10i_sampling_type={}_k={}_omega=1.25_theta=0.1'.format(sampling_scheme,total_samples))
pio.write_image(fig , path, 'png')

# fig.show()
