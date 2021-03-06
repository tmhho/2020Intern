import pandas as pd
import plotly.graph_objects as go
import glob
import sys
import os
import plotly.io as pio
filenames = os.path.join('csv-files','*_theta=1.0.csv')
filenames = glob.glob(filenames)
print(filenames)
data = []
sampling_schemes = []
for file in filenames:
    sampling_schemes += [file.split('_')[4].split('=')[1].split('.')[0]]
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
    title='Camparison of runtime of different sampling sampling_schemes, M=1.0, 500 000 segsites, 10 islands, theta = 1.0',
    xaxis_title='samples size',
    yaxis_title='runtime',
    yaxis_type='log' 
)
if not os.path.exists('graphs'):
    os.mkdir('graphs')
path = os.path.join('graphs', 'Comparison-of-runtime_10i_k=8_500000segsites_M1.0_theta=1.0.png')
pio.write_image(fig , path, 'png')
# fig.show()
