from ms2afs import _execute
import plotly.graph_objects as go
import time
list_omega = [0.4,0.8,1.2,1.5,1.6, 1.9]
samples_size = 6
num_islands = 10
migration_rate = 1.0
deme_size = 1.0
runtime = []
for omega in list_omega:
	qmd_cmd = ['./qmd', str(samples_size), str(num_islands), str(migration_rate), str(deme_size),str(samples_size),'0', '0', '0', '0','0','0','0', '0', '0', str(omega)]
	print(qmd_cmd)
	 
	start_time = time.time()
	for line in _execute(qmd_cmd):
		print(line)
	runtime.append(time.time()-start_time)

fig=go.Figure()
fig.add_trace(go.Scatter(x=list_omega,y=runtime,mode='lines+markers'))
fig.update_layout(
	title='M=1.0 k=6 num_islands=10',
	xaxis_title='omega',
	yaxis_title='run time')
fig.show()