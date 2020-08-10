import afstools
import ms2afs
import time
import sys
import os
import numpy as np
import glob
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go

nsegsites = 50000
k = [ 
    4,
    6,
    8,
    10,
    12,
    # 14,
    # 16,
    # 18
]

migration_rate = 1.0
sampling_type = sys.argv[1]
mutation_rate = 1.0
list_islands = [5,10,15,20]

deme_size = 1.0
omega = 1.25


afs_runtimes = [['samples_size']+k]

for num_islands in list_islands: 
  print('num_islands: ', num_islands)
  runtime_ms = []
  runtime_qmd = []
  for total_samples in k:
      sampling = afstools.sampling_scheme(total_samples,sampling_type)
      print('          sampling: ', sampling)

      # measure ms runtime
      start_time = time.time()
      ms_afs = ms2afs.get_nisland_afs(num_islands, migration_rate, sampling, 
          mutation_rate, 10 * nsegsites, max_sites =nsegsites, step = 100)
      runtime_ms.append(time.time() - start_time)

      # measure qmd runtime
      start_time = time.time()
      qmd_afs = afstools.expected_nisland_afs(sampling, 
        num_islands, migration_rate, deme_size, omega)
      runtime_qmd.append(time.time() - start_time)

  afs_runtimes.append([f'{num_islands}i_ms_runtime']  + runtime_ms) 
  afs_runtimes.append([f'{num_islands}i_qmd_runtime'] + runtime_qmd)

afs_runtimes = afstools.transposed(afs_runtimes)
datetime = afstools.datetime_tag()
output_filename = os.path.join('csv-files', f'{datetime}_runtimes_sampling={sampling_type}_omega={omega}_theta={mutation_rate}_M={migration_rate}.csv')
afstools.write_csv(afs_runtimes, output_filename, ',')

# #######DRAWING GRAPH#########
filename = os.path.join('csv-files',f'*_runtimes_sampling={sampling_type}_omega={omega}_theta={mutation_rate}_M={migration_rate}.csv')
file = glob.glob(filename)[0]
data = pd.read_csv(file)

fig = go.Figure()
for num_islands in list_islands:
  fig.add_trace(go.Scatter(x=list(data['samples_size']),
                               y=list(data[f'{num_islands}i_qmd_runtime']),
                               mode='lines+markers',
                               marker=dict(opacity=0.5),
                               name=f'{num_islands} islands'))

   
fig.update_layout(
  title=f'Compare runtime of different numbers of islands: sampling_scheme = {sampling_type} M={migration_rate}',
  xaxis_title='samples size',
  yaxis_title='runtime (s)', 
  yaxis_type='log')
# fig.show()

###############SAVE FIGURE######################################
if not os.path.exists('graphs'):
  os.mkdir('graphs')
if not os.path.exists('html-files'):
  os.mkdir('html-files')
path_png = os.path.join ('graphs', 'Compare_runtime_nums_islands_'+ file[10:-4] + '.png')
path_html = os.path.join('html-files','Compare_runtime_nums_islands_'+ file[10:-4] + '.html')
pio.write_image(fig, path_png, format='png')
fig.write_html(path_html)