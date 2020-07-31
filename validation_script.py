import ms2afs
import os
import csv
import time
import sys
import afstools
import numpy as np

def sampling_scheme (total_samples, type):
    if type == 'half-half':
        if (total_samples//2) % 2 == 0:
            return [total_samples//2]*2
        else:
            return [(total_samples//2)+1, (total_samples//2)-1]
    if type == 'concentrated':
        return [total_samples]
    if type == 'spread':
        return [2]*int((total_samples//2))

# reps = [
#     500,
#     1000,
#     5000,
#     10000,
#     50000,
#     100000,
#     500000,
#     1000000
# ]
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

migration_rates = np.linspace(start=0.05, stop = 100.0, num = 25)
total_samples = int(sys.argv[1])
sampling_type = sys.argv[2]
mutation_rate = 0.1
islands = 10

#PANMICTIC AFS
panmictic_afs = afstools.expected_panmictic_afs(total_samples)


#runtime = []

afs_table = [
    ['panmictic_afs'] + panmictic_afs
]

samples = sampling_scheme(total_samples, sampling_type)
   
afs_distances= [['num_segsites'] + list_nsegsites]
for migration_rate in migration_rates:
    qmd_afs = afstools.expected_nisland_afs(samples = samples, 
    islands = islands, migration = migration_rate, deme = 1.0, omega = 1.25)
    print(f'qmd_afs: {qmd_afs}')
    average_abs_err = []
    rel_err = []
    i = 0
    while i < len(list_nsegsites):

        num_segsites = list_nsegsites[i]
        nreps = 10* num_segsites
        ms_observed_afs = ms2afs.get_nisland_afs(islands= islands, migration = migration_rate,
            samples =samples, theta = mutation_rate, repetitions = nreps, max_sites = num_segsites, step = 1)
        ms_observed_afs = [ i/ sum(ms_observed_afs) for i in ms_observed_afs]
        print(f'ms_observed_afs{ms_observed_afs}')
        afs_table.append( 
            [f'observed_afs_M{migration_rate}_nsegsites{num_segsites}'] + ms_observed_afs
        )

        average_abs_err.append(afstools.average_absolute_error(ms_observed_afs, qmd_afs))
        rel_err.append(afstools.relative_error(ms_observed_afs, qmd_afs))
       
        i += 1
    afs_distances += [
        [f'average.abs.error_{migration_rate}']  + average_abs_err,
        [f'rel.error_{migration_rate}']  + rel_err,
    ]
    afs_table.append([f'expected_afs_M{migration_rate}'] + qmd_afs)
    print(f'afs_distances: {afs_distances}')
afs_distances = afstools.transposed(afs_distances)
afs_table = afstools.transposed(afs_table)
version = sys.argv[3]
output_afs_distances = os.path.join('csv-files', f'afs_errors_k={total_samples}_10i_sampling={sampling_type}_omega=1.25_theta=0.1_{version}.csv')
output_afs_table = os.path.join('csv-files', f'afs_values_k={total_samples}_10i_sampling={sampling_type}_omega=1.25_theta=0.1_{version}.csv')
afstools.write_csv(afs_table, output_afs_table, ',')
afstools.write_csv(afs_distances, output_afs_distances,',')
