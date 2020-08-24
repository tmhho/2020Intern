from numpy import loadtxt
import plotly.graph_objects as go
import afstools 
import sys
import ms2afs
import os

lines = loadtxt("FoldSFS_YRI.txt", delimiter ="\t", unpack = False)
afs = [line[1] for line in lines]
# subsampled_yri_afs = afstools.subsample(afs,6)
yri_afs = afstools.normalized(afs)[0]
# graphically_transformed_yri_afs = afstools.graphical_transform(yri_afs)

# fig=go.Figure()
# fig = afstools.visualize_afs(afs= graphically_transformed_yri_afs, namefile = 'yri_afs',fig = fig, nameline = 'yri_afs')


num_islands = ['5'
, '10' 
,'20'
]
list_T =['1'
,'5'
,'10'
]
list_x = ['0.1'
, '0.01'
, '0.5'
]
migration_rates = ['0.1'
,'1.0'
,'10.0'
]

data = afstools.simulated_nislands_size_inscreased_all_islands(yri_afs = yri_afs, num_islands=num_islands, list_T =list_T, list_x = list_x,migration_rates = migration_rates, nreps = '30000000')
# print(data)
filename = os.path.join('json-files', 'yri-afs_' + afstools.datetime_tag() + '_values.json')
afstools.write_json(data, filename)
keys = list(data.keys())
dict_distances = {'model': 'Distances between yri_afs and nislands size increased in all islands model afs'}
for key in keys[1:]:
	afs = data[key]
	dict_distances[key] = afstools.average_absolute_error(yri_afs,afs)
print(dict_distances)
filename1 = os.path.join('json-files', 'yri-afs_' + afstools.datetime_tag() + '_distances.json')
afstools.write_json(dict_distances, filename1)

# afs = data['5islands_1T_0.1x_0.1M']
# graphically_transformed_afs = afstools.graphical_transform(afs)
# # print(afs)
# fig = afstools.visualize_afs(afs= graphically_transformed_afs, namefile = 'yri_afs',fig = fig, nameline = 'nislands_size_inscreased_all_islands:5i_1T_0.1x_0.1M', show=True)

