import pandas as pd
import glob
import plotly.graph_objects as go

filenames = glob.glob('afs_distances_k=6_M*')
filenames.sort()
M = [float(name.split('_')[3].split('=')[1]) for name in filenames]
#filenames = ['afs_distances_k=6_M=0.01_10i.csv','afs_distances_k=6_M=0.1_10i.csv','afs_distances_k=6_M=1_10i.csv','afs_distances_k=6_M=10_10i.csv']

#combined_csv = pd.concat( [ pd.read_csv(f) for f in filenames ], sort=False )
#combined_csv.to_csv( "validation.csv", index=False )

###################TRANPOSE CSV FILE###########################
# for file in filenames: 
#     pd.read_csv(file, header=None).T.to_csv( 'transposed.{}'.format(file), header=False, index=False)

# transposed_filenames = glob.glob('transposed.afs_distances_k=6_M*')

data = []
for file in filenames :
    data.append([pd.read_csv(file)])
    
# data1= pd.read_csv("transposed.afs_distances_k=6_M=0.01_10i.csv")
# data2= pd.read_csv("transposed.afs_distances_k=6_M=0.1_10i.csv")
# data3= pd.read_csv("transposed.afs_distances_k=6_M=1_10i.csv")
# data4= pd.read_csv("transposed.afs_distances_k=6_M=10_10i.csv")

#####################DRAWING GRAPH##############################
fig = go.Figure()

#color = ['firebrick','royalblue','yellow','green']

for i in range(len(data)):
	fig.add_trace(go.Scatter(
		x=list(data[i][0]['repetitions']),
		y = list(data[i][0]['abs.error_{}'.format(M[i])]),
		mode='lines',
		name='abs.error_{}'.format(M[i])))
   
fig.update_layout(
	title='Validation: nislands = 10, k=6',
	xaxis_title='nreps',
	yaxis_title='abs_error', 
	xaxis_type='log')
fig.show()
