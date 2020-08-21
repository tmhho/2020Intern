from numpy import loadtxt
import plotly.graph_objects as go
import afstools 
import sys
import ms2afs

lines = loadtxt("FoldSFS_YRI.txt", delimiter ="\t", unpack = False)
afs = [line[1] for line in lines]
# subsampled_yri_afs = afstools.subsample(afs,6)
yri_afs = afstools.normalized(afs)[0]
yri_afs = afstools.graphical_transform(yri_afs)

# fig=go.Figure()
# fig = visualize_afs(afs= yri_afs, namefile = 'yri_afs',fig = fig, nameline = 'yri_afs')


num_islands = ['5'
# , '10' 
# ,'20'
]
list_T =['1'
# ,'5'
# ,'10'
]
list_x = ['0.1'
# , '0.01'
# , '0.5'
]
migration_rates = ['0.1'
# ,'1.0'
# ,'10.0'
]

data = {'model': 'Nislands-model with population size increased in all islands'} 
afs = afstools.simulated_nislands_size_inscreased_all_islands(num_islands=num_islands, list_T =list_T, list_x = list_x,migration_rates = migration_rates, nreps = '30000')
print(afs.keys())

