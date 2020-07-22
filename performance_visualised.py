import pandas as pd
import plotly.graph_objects as go
import glob

filenames = glob.glob('afs_distances_M*')
M = [float(name.split('_')[2].split('=')[1]) for name in filenames]

# filenames = ['afs_distances_M=0.1_10i.csv','afs_distances_M=1_10i.csv','afs_distances_M=10_10i.csv']

# combined_csv = pd.concat( [ pd.read_csv(f) for f in filenames ], sort=False )
# combined_csv.to_csv( "runtime_Mvar.csv", index=False )
# pd.read_csv("runtime_Mvar.csv", header=None).T.to_csv( "transposed.runtime_Mvar.csv", header=False, index=False)
# data = pd.read_csv("transposed.runtime_Mvar.csv")
data = []
for file in filenames :
    data.append([pd.read_csv(file)])

fig = go.Figure()
# M = [0.1,1,10]
color = ['firebrick','royalblue','orange', 'purple']
for i in range(len(M)):
    fig.add_trace(go.Scatter(x=list(data[i][0]['samples_size']),
                             y=list(data[i][0]['ms_runtime_M={}'.format(M[i])]),
                             mode='lines+markers',
                             line=dict(color=color[i], 
                                width=2),
                             name='ms_runtime_M={}'.format(M[i])))
    fig.add_trace(go.Scatter(x=list(data[i][0]['samples_size']),
                             y=list(data[i][0]['qmd_runtime_M={}'.format(M[i])]),
                             mode='lines',
                             line=dict(color=color[i], width=2, dash='dash'),
                             name='qmd_runtime_M={}'.format(M[i])))
fig.update_layout(
    title='Performance, nreps = 1M, 10 islands',
    xaxis_title='samples size',
    yaxis_title='runtime',
    yaxis_type='log' 
)
fig.show()
