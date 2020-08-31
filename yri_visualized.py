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
keys = list(data.keys())[1:]
distances = []
dict_distances = {}

num_islands = [
'5'
# ,'10' 
# '20'
]
list_T =['1'
,'5'
,'10'
]
list_x = ['0.01'
, '0.1'
, '0.5'
]
migration_rates = ['0.1'
,'1.0'
,'10.0'
]
dict_data = {}
dict_distances = {}
distances = []
for islands in num_islands:
	for T in list_T:
		for x in list_x:	
			for M in migration_rates:
				key = f'{islands}islands_{T}T_{x}x_{M}M'
				afs = data[key]
				distance = afstools.average_absolute_error(yri_afs, afs)
				dict_distances[key] = distance
				distances.append(distance)	
				afs = afstools.graphical_transform(afs)
				fig = afstools.visualize_afs(afs= afs, namefile = 'yri_afs',fig = fig, nameline = key)

fig.show()
html_file = os.path.join('html-files', 'yri_afs_nislands_all_increased_pop_5i_' + afstools.datetime_tag()+ '.html')
pio.write_html(fig, html_file)

######HEAT MAP
list_x = ['0.01'
, '0.1'
, '0.5'
]
migration_rates = ['0.1'
,'1.0'
,'10.0'
]

fig2 = go.Figure(data=go.Heatmap(
	z = [distances[n:n+3] for n in range(0, 9, 3)],
	x = [f'M = {M}' for M in migration_rates],
	y = [f'x = {x}' for x in list_x],
	hoverongaps = False))

fig2.show()
filename2 = os.path.join('graphs', 'fixed5i_1T_' + afstools.datetime_tag() + '_distances.png')
pio.write_image(fig2, filename2, 'png')

html_file2 = os.path.join('html-files', 'heatmap_yri_afs_nislands_all_increased_pop_5i_1T' + afstools.datetime_tag()+ '.html')
pio.write_html(fig2, html_file2)



#########HEATMAP
T ='1'
x = '0.1'
num_islands = [
'5'
,'10' 
,'20'
]
migration_rates = ['0.1'
,'1.0'
,'10.0'
]
distances2=[]
dict_distances={}
for islands in num_islands:		
	for M in migration_rates:
		key = f'{islands}islands_{T}T_{x}x_{M}M'
		afs = data[key]
		distance = afstools.average_absolute_error(yri_afs, afs)
		dict_distances[key] = distance
		distances2.append(distance)	
		afs = afstools.graphical_transform(afs)
		fig = afstools.visualize_afs(afs= afs, namefile = 'yri_afs',fig = fig, nameline = key)
print(dict_distances)
filename3 = os.path.join('json-files', 'yri-afs_' + afstools.datetime_tag() + '_distances.json')
afstools.write_json(dict_distances, filename3)

html_file = os.path.join('html-files', 'yri_afs_nislands_all_increased_pop_1T_0.1x_' + afstools.datetime_tag()+ '.html')
pio.write_html(fig, html_file)

fig3 = go.Figure(data=go.Heatmap(
	z = [distances2[n:n+3] for n in range(0, 9, 3)],
	y = [f'M = {M}' for M in migration_rates],
	x = [f'num_islands = {i}' for i in num_islands],
	hoverongaps = False))
# fig3.show()
filename3 = os.path.join('graphs', 'fixed5i_0.1T_' + afstools.datetime_tag() + '_distances.png')
pio.write_image(fig3, filename3, 'png')

html_file3 = os.path.join('html-files', 'heatmap_yri_afs_nislands_all_increased_pop_1T_0.1x_' + afstools.datetime_tag()+ '.html')
pio.write_html(fig3, html_file3)