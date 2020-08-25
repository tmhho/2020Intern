import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import sys
import os
from numpy import loadtxt 
import afstools

lines = loadtxt("FoldSFS_YRI.txt", delimiter ="\t", unpack = False)
afs = [line[1] for line in lines]
yri_afs = afstools.normalized(afs)[0]

graphically_transformed_yri_afs = afstools.graphical_transform(yri_afs)
fig=go.Figure()
fig = afstools.visualize_afs(afs= graphically_transformed_yri_afs, namefile = 'yri_afs',fig = fig, nameline = 'yri_afs')

# argv[1] is the lastest file in json-files folder 
json_filename = os.path.join('json-files', sys.argv[1])
data = afstools.read_json(json_filename)
keys = list(data.keys())[1:][:-1]

dict_distances = {}
for key in keys:
	afs = data[key]
	dict_distances[key] = afstools.average_absolute_error(afs,yri_afs)
	afs = afstools.graphical_transform(afs)
	fig = afstools.visualize_afs(afs= afs, namefile = 'yri_afs',fig = fig, nameline = key)
fig.show()
print(dict_distances)
filename1 = os.path.join('json-files', 'yri-afs_' + afstools.datetime_tag() + '_distances.json')
afstools.write_json(dict_distances, filename1)