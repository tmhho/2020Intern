import plotly.graph_objects as go
import pandas as pd
import glob
import sys
import os
import plotly.io as pio
import numpy as np

total_samples = int(sys.argv[1])
sampling_scheme = sys.argv[2]
filename = os.path.join('csv-files','*_values_k={}_10i_sampling={}_omega=1.25_theta=0.1.csv'.format(total_samples,sampling_scheme))
file = glob.glob(filename)[0]

#!!! SAME list_M as validation_script.py 

migration_rates = np.logspace(start=-2, stop = 1, num = 10)


data = pd.read_csv(file)

list_c=[]

for i in range(0,total_samples-1):
    c = [data[f'expected_afs_M{M}'][i]/data['panmictic_afs'][i] for M in migration_rates]
    list_c.append(c)

fig = go.Figure()
for i in range(total_samples-1):
        fig.add_trace(go.Scatter(
    x=migration_rates, y=list_c[i],
    mode='lines+markers',
    line=dict(width=0.5
        ),
    name = 'c{}'.format(i+1)# define stack group
))


fig.update_layout(title='Afs, k={},nislands=10, sampling_scheme={}'.format(total_samples,sampling_scheme), 
    xaxis_type='log', xaxis_title='migration rate')
if not os.path.exists('graphs'):
    os.mkdir('graphs')
path = os.path.join('graphs', 'Converge1'+file[10:-4]+'.png')
pio.write_image(fig , path, 'png')

# fig.show()
