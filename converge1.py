import plotly.graph_objects as go
import pandas as pd
import glob
import sys
import os
import plotly.io as pio

total_samples = int(sys.argv[1])
sampling_scheme = sys.argv[2]
filename = os.path.join('csv-files','afs_values_k={}_10i_sampling={}.csv'.format(total_samples,sampling_scheme))

list_M = [0.1, 1.0, 10.0]

data = pd.read_csv(filename)

list_c=[]

for i in range(0,total_samples-1):
    c = [data['observed_afs_M{}_nreps1000000'.format(M)][i]/data['panmictic_afs'][i] for M in list_M]
    list_c.append(c)

fig = go.Figure()
for i in range(total_samples-1):
        fig.add_trace(go.Scatter(
    x=list_M, y=list_c[i],
    mode='lines+markers',
    line=dict(width=0.5
        # , color='rgb(131, 90, 241)'
        ),
    name = 'c{}'.format(i+1)# define stack group
))


fig.update_layout(title='Afs, k={},nislands=10, sampling_scheme={}'.format(total_samples,sampling_scheme), 
    xaxis_type='log', xaxis_title='M')
if not os.path.exists('graphs'):
    os.mkdir('graphs')
path = os.path.join('graphs', 'Converge1:nreps=1000000_10i_sampling_type={}_k={}'.format(sampling_scheme,total_samples))
pio.write_image(fig , path, 'png')

# fig.show()
