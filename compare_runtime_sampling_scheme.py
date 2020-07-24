import pandas as pd
import plotly.graph_objects as go
import glob
import sys

filenames = glob.glob('afs_runtimes_n=10_w=1.25_sampling=*')
print(filenames)
sampling_schemes = [(name.split('_')[4].split('=')[1].split('.')[0]) for name in filenames]


data = []

for file in filenames :
    data.append([pd.read_csv(file)])

fig = go.Figure()

color = ['firebrick','royalblue','orange', 'purple']
for i in range(len(sampling_schemes)):
    fig.add_trace(go.Scatter(x=list(data[i][0]['samples_size']),
                             y=list(data[i][0]['ms_runtime_M1.0']),
                             mode='lines+markers',
                             # line=dict(color=color[i], 
                             #    width=2),
                             name='ms_runtime_sampling:{}'.format(sampling_schemes[i])))

fig.update_layout(
    title='Camparison of runtime of different sampling sampling_schemes, M=1.0, 500 000 reps, 10 islands',
    xaxis_title='samples size',
    yaxis_title='runtime',
    yaxis_type='log' 
)
fig.show()
