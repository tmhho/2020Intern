from numpy import loadtxt
import plotly.graph_objects as go
import afstools 
import sys
import ms2afs
import os

data = afstools.read_json('json-files/yri-afs-2908.json')

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
for islands in num_islands:
	for T in list_T:
		for x in list_x:	
			for M in migration_rates:
				dict_data[f'{islands}islands_{T}T_{x}x_{M}M'] = data[f'{islands}islands_{T}T_{x}x_{M}M']

afstools.write_json(dict_data, 'json-files/yri_afs_2908_values.json')