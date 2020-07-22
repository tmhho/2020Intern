import plotly.graph_objects as go
import pandas as pd
import glob

filenames = glob.glob('afs_values_k=6_M*')
filenames.sort()
M = [float(name.split('_')[3].split('=')[1]) for name in filenames]

# combined_csv = pd.concat( [ pd.read_csv(f) for f in filenames ], sort=False )
# combined_csv.to_csv( "validation.csv", index=False )

###################TRANPOSE CSV FILE###########################
# for file in filenames: 
#     pd.read_csv(file, header=None).T.to_csv( 'transposed.{}'.format(file), header=False, index=False)

# transposed_filenames = glob.glob('transposed.afs_values_k=6_M*')

data = []
for file in filenames :
    data.append([pd.read_csv(file)])

list_c=[]
k = len(data[1][0]['observed 1000000'])

for i in range(k):
    c = [afs[0]['observed 1000000'][i] for afs in data]
    list_c.append(c)
fig = go.Figure()
for i in range(len(list_c)):
        fig.add_trace(go.Scatter(
    x=M, y=list_c[i],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5
        # , color='rgb(131, 90, 241)'
        ),
    stackgroup='one',
    name = 'c{}'.format(i+1)# define stack group
))
# fig.add_trace(go.Scatter(
#     x=x, y=v[1],
#     hoverinfo='x+y',
#     mode='lines',
#     line=dict(width=0.5, color='rgb(111, 231, 219)'),
#     stackgroup='one',
#     name='c2'
# ))
# fig.add_trace(go.Scatter(
#     x=x, y=v[2],
#     hoverinfo='x+y',
#     mode='lines',
#     line=dict(width=0.5, color='rgb(184, 247, 212)'),
#     stackgroup='one',
#     name='c3'
# ))
# fig.add_trace(go.Scatter(
#     x=x, y=v[3],
#     hoverinfo='x+y',
#     mode='lines',
#     line=dict(width=0.5, color='rgb(183, 132, 167)'),
#     stackgroup='one',
#     name='c4'
# ))
# fig.add_trace(go.Scatter(
#     x=x, y=v[4],
#     hoverinfo='x+y',
#     mode='lines',
#     line=dict(width=0.5, color='rgb(252, 190, 17)'),
#     stackgroup='one',
#     name='c5'
# ))

fig.update_layout(title='Afs, k=6, nislands=10', xaxis_type='log', xaxis_title='M')


fig.show()
