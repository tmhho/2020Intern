import ms2afs
import os
import csv
import time
import sys
import afstools
import numpy as np
import afstools

list_nsegsites = [
    500,
    1000,
    5000,
    10000,
    50000,
    100000,
    500000,
    # 1000000
]

migration_rates = np.logspace(start=-2, stop = 1, num = 10)
total_samples = int(sys.argv[1])
sampling_type = sys.argv[2]
mutation_rate = 0.1
islands = 10
versions = list(range(1,4))

#PANMICTIC AFS
panmictic_afs = afstools.expected_panmictic_afs(total_samples)


#runtime = []

afs_table = [
    ['panmictic_afs'] + panmictic_afs
]

samples = afstools.sampling_scheme(total_samples, sampling_type)
afs_distances= [['num_segsites'] + list_nsegsites]

for migration_rate in migration_rates:
    qmd_afs = afstools.expected_nisland_afs(samples = samples, 
    islands = islands, migration = migration_rate, deme = 1.0, omega = 1.25)
    print(f'Migration rate {migration_rate} with qmd_afs: {qmd_afs}')
    afs_table.append([f'expected_afs_M{migration_rate}'] + qmd_afs)

    

    for version in versions : 
        print('     starting version: ', version)
        i = 0
        average_abs_err = []
        rel_err = []
        while i < len(list_nsegsites):
            num_segsites = list_nsegsites[i]
            print('         segsite: ',num_segsites)
            nreps = 10* num_segsites
            ms_observed_afs = ms2afs.get_nisland_afs(islands= islands, migration = migration_rate,
                samples =samples, theta = mutation_rate, repetitions = nreps, max_sites = num_segsites, step = 100)
            
            ms_observed_afs = afstools.normalized(ms_observed_afs)[0]
            print('           ms_observed_afs', ms_observed_afs)
            afs_table.append( 
                [f'ver{version}_observed_afs_M{migration_rate}_nsegsites{num_segsites}'] + ms_observed_afs
            )

            average_abs_err.append(afstools.average_absolute_error(ms_observed_afs, qmd_afs))
            rel_err.append(afstools.relative_error(ms_observed_afs, qmd_afs))
            
            i += 1
        afs_distances += [
                [f'ver{version}_average.abs.error_M{migration_rate}']  + average_abs_err,
                [f'ver{version}_rel.error_M{migration_rate}']  + rel_err,
            ]
        
afs_distances = afstools.transposed(afs_distances)
afs_table = afstools.transposed(afs_table)

datetime = afstools.datetime_tag()
name_afs_distances = os.path.join('csv-files', f'{datetime}_errors_k={total_samples}_{islands}i_sampling={sampling_type}_omega=1.25_theta=0.1.csv')
name_afs_table = os.path.join('csv-files', f'{datetime}_values_k={total_samples}_{islands}i_sampling={sampling_type}_omega=1.25_theta=0.1.csv')
afstools.write_csv(afs_table, name_afs_table, ',')
afstools.write_csv(afs_distances, name_afs_distances,',')
    