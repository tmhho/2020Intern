import numpy as np
import time
import os

import afstools

list_omega = np.linspace(0.1, 1.9, num = 25)
sampling = [6]
num_islands = 10
migration_rate = 1.0
deme_size = 1.0

sampling_string = '-'.join(str(ki) for ki in sampling)
runtime = []
for omega in list_omega:
	start_time = time.time()
	qmd_afs = afstools.expected_nisland_afs(sampling, num_islands, migration_rate, deme_size, omega)
	runtime.append(time.time() - start_time)

table = [
	['omega'] + list(list_omega),
	['run time'] + runtime
]

table = afstools.transposed(table)
output_filename = os.path.join('csv-files', f'timing_qmd_M{migration_rate}_n{num_islands}_s{sampling_string}.csv')
afstools.write_csv(table, output_filename, ',')

try:
	import plotly.graph_objects as go
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=list_omega, y=runtime, mode='lines+markers'))
	fig.update_layout(
		title = f'M = {migration_rate}; sampling = {sampling}; n = {num_islands}',
		xaxis_title = 'omega',
		yaxis_title = 'run time (seconds)')
	fig.show()
except:
	print('Error: could not load plotting library!')