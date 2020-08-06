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
    # 10000,
    # 50000,
    # 100000,
    # 500000,
    # 1000000
]

results_dir = 'csv-files'

total_samples = int(sys.argv[1])
sampling_type = sys.argv[2]
islands = int(sys.argv[3])

migration_rates = [0.1, 1, 10]
mutation_rate = 1
versions = 3
omega = 1.25

samples = afstools.sampling_scheme(total_samples, sampling_type)
afs_distances = [['num_segsites'] + list_nsegsites]
afs_table = []

for migration_rate in migration_rates:
    print(f'Starting migration rate {migration_rate}')

    qmd_afs = afstools.expected_nisland_afs(
        samples = samples, 
        islands = islands, 
        migration = migration_rate, 
        deme = 1.0, 
        omega = omega
    )
    afs_table.append([f'expected_afs_M{migration_rate}'] + qmd_afs)
    print('Exact expected afs:', qmd_afs)

    for version in range(versions): 
        print(f'     starting iteration {version + 1} of {versions}')

        average_abs_err = []
        rel_err = []
        for num_segsites in list_nsegsites:
            print(f'         simulating {num_segsites} ms segsites')
            nreps = 10 * num_segsites
            ms_observed_afs = ms2afs.get_nisland_afs(
                islands = islands, 
                migration = migration_rate,
                samples = samples, 
                theta = mutation_rate, 
                repetitions = nreps, 
                max_sites = num_segsites, 
                step = 100
            )
            
            ms_observed_afs = afstools.normalized(ms_observed_afs)[0]
            print('           Observed simulated afs:', ms_observed_afs)
            afs_table.append( 
                [f'ver{version}_observed_afs_M{migration_rate}_nsegsites{num_segsites}'] + ms_observed_afs
            )

            average_abs_err.append(afstools.average_absolute_error(ms_observed_afs, qmd_afs))
            rel_err.append(afstools.relative_error(ms_observed_afs, qmd_afs))
        
        afs_distances += [
            [f'ver{version}_average.abs.error_M{migration_rate}']  + average_abs_err,
            [f'ver{version}_rel.error_M{migration_rate}']  + rel_err,
        ]
        
datetime = afstools.datetime_tag()
basename = f'afs_validation_nisland_{datetime}_'

afs_distances = afstools.transposed(afs_distances)
name_afs_distances = os.path.join(results_dir, basename + 'distances.csv')
afstools.write_csv(afs_distances, name_afs_distances, ',')

afs_table = afstools.transposed(afs_table)
name_afs_table = os.path.join(results_dir, basename + 'raw.csv')
afstools.write_csv(afs_table, name_afs_table, ',')

afs_settings = {
    "basename" : basename,
    "distances filename" : name_afs_distances,
    "raw data filename" : name_afs_table,
    "segsites" : list_nsegsites,
    "total samples" : total_samples,
    "sampling type" : sampling_type,
    "number of islands" : islands,
    "migration rates" : migration_rates,
    "theta" : mutation_rate,
    "iterations" : versions,
    "omega" : omega,
    "sampling vector" : samples
}

name_afs_settings = os.path.join(results_dir, basename + 'settings.json')
afstools.write_json(afs_settings, name_afs_settings)