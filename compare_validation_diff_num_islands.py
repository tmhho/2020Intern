import ms2afs
import os
import csv
import time
import sys
import afstools
import numpy as np
import afstools
import plotly.io as pio
import pandas as pd
import glob
import plotly.graph_objects as go

list_nsegsites = [
    500,
    1000,
    5000,
    10000,
    50000,
    100000,
    500000,
    1000000
]

migration_rates = np.logspace(start=-2, stop = 1, num = 3)
total_samples = int(sys.argv[1])
sampling_type = sys.argv[2]
mutation_rate = 0.1
list_islands = [5,10,15,20]


#PANMICTIC AFS
panmictic_afs = afstools.expected_panmictic_afs(total_samples)


#runtime = []

afs_table = [
    ['panmictic_afs'] + panmictic_afs
]

samples = afstools.sampling_scheme(total_samples, sampling_type)
afs_distances= [['num_segsites'] + list_nsegsites]

for islands in list_islands : 
    print('num_islands: ', islands)
    
    for migration_rate in migration_rates:
        qmd_afs = afstools.expected_nisland_afs(samples = samples, 
        islands = islands, migration = migration_rate, deme = 1.0, omega = 1.25)
        print(f'Migration rate {migration_rate} with qmd_afs: {qmd_afs}')
        afs_table.append([f'expected_afs_M{migration_rate}'] + qmd_afs)

        average_abs_err = []
        rel_err = []
        i = 0 
        while i < len(list_nsegsites):
            num_segsites = list_nsegsites[i]
            print('         segsite: ',num_segsites)
            nreps = 10* num_segsites
            ms_observed_afs = ms2afs.get_nisland_afs(islands= islands, migration = migration_rate,
                samples =samples, theta = mutation_rate, repetitions = nreps, max_sites = num_segsites, step = 100)
            
            ms_observed_afs = afstools.normalized(ms_observed_afs)[0]
        # print('              ms_observed_afs', ms_observed_afs)
            afs_table.append( 
                [f'{islands}i_observed_afs_M{migration_rate}_nsegsites{num_segsites}'] + ms_observed_afs
            )

            average_abs_err.append(afstools.average_absolute_error(ms_observed_afs, qmd_afs))
            rel_err.append(afstools.relative_error(ms_observed_afs, qmd_afs))
            
            i += 1
        afs_distances += [
                [f'{islands}i_average.abs.error_M{migration_rate}']  + average_abs_err,
                [f'{islands}i_rel.error_M{migration_rate}']  + rel_err,
            ]
        
afs_distances = afstools.transposed(afs_distances)
afs_table = afstools.transposed(afs_table)

datetime = afstools.datetime_tag()
name_afs_distances = os.path.join('csv-files', f'{datetime}_errors_k={total_samples}_sampling={sampling_type}_omega=1.25_theta=0.1.csv')
name_afs_table = os.path.join('csv-files', f'{datetime}_values_k={total_samples}_sampling={sampling_type}_omega=1.25_theta=0.1.csv')
afstools.write_csv(afs_table, name_afs_table, ',')
afstools.write_csv(afs_distances, name_afs_distances,',')

#######DRAWING GRAPH#####################

filename = os.path.join('csv-files',f'*_errors_k={total_samples}_sampling={sampling_type}_omega=1.25_theta=0.1.csv')
file = glob.glob(filename)[0]

data = pd.read_csv(file)
fig=go.Figure()
migration_rate = migration_rates[1]
for islands in list_islands :
    fig.add_trace(go.Scatter(
        x=list(data['num_segsites']),
        y = list(data[f'{islands}i_average.abs.error_M{migration_rate}']),
        mode='lines+markers',
        name = f'{islands} islands'))

fig.update_layout(
    title=f'Compare accuracy of different numbers of islands: k={total_samples} sampling_scheme = {samples} migration_rate = {migration_rate}',
    xaxis_title='num_segsites',
    yaxis_title='average_abs_error', 
    xaxis_type='log',
    yaxis_type='log')
# fig.show()
###############SAVE FIGURE######################################
if not os.path.exists('graphs'):
    os.mkdir('graphs')

path_png = os.path.join ('graphs', 'Compare_accuracy_'+ file[10:-4] + '.png')
pio.write_image(fig, path_png, format='png')
