import pandas as pd
import plotly.graph_objects as go
import glob
import sys
import os
import plotly.io as pio
sampling_scheme = sys.argv[1]
filenames = os.path.join('csv-files',f'afs_runtimes_10i_w=1.25_sampling={sampling_scheme}_omega=1.25_theta=*')
filenames = glob.glob(filenames)
print(filenames)
data = []
thetas = []
for file in filenames:
    thetas += [file.split('_')[6].split('=')[1][:-4]]
    data.append([pd.read_csv(file)])

fig = go.Figure()

color = ['firebrick','royalblue','orange', 'purple']
for i in range(len(thetas)):
    fig.add_trace(go.Scatter(x=list(data[i][0]['samples_size']),
                             y=list(data[i][0]['ms_runtime_M1.0']),
                             mode='lines+markers',
                             # line=dict(color=color[i], 
                             #    width=2),
                             name='ms_runtime_theta={}'.format(thetas[i])))

fig.update_layout(
    title='Camparison of runtime of different theta, sampling_scheme= {sampling_scheme}, M=1.0, 500 000 segsites, 10 islands',
    xaxis_title='samples size',
    yaxis_title='runtime',
    yaxis_type='log' 
)
if not os.path.exists('graphs'):
    os.mkdir('graphs')
path = os.path.join('graphs', f'Comparison-of-runtime_10i_k=8_500000segsites_M1.0_sampling={sampling_scheme}.png')
pio.write_image(fig , path, 'png')
# fig.show()
