import afstools
import ms2afs
import time
import sys
import os

nreps = 500_000
k = [ 
    4,
    6,
    8,
    10,
    12,
    14,
    # 16,
    # 18
]

migration_rate = float(sys.argv[1])
mutation_rate = 0.1
num_islands = 10
deme_size = 1.0
omega = 1.25

runtime_ms = []
runtime_qmd = []
for total_samples in k:
    sampling = [total_samples]
    print(f'sampling:', sampling)

    # measure ms runtime
    start_time = time.time()
    ms_afs = ms2afs.get_nisland_afs(num_islands, migration_rate, sampling, mutation_rate, 10 * nreps, nreps)
    runtime_ms.append(time.time() - start_time)

    # measure qmd runtime
    start_time = time.time()
    qmd_afs = afstools.expected_nisland_afs(sampling, num_islands, migration_rate, deme_size, omega)
    runtime_qmd.append(time.time() - start_time)

afs_runtimes = [
    ['samples_size'] + k,
    ['ms_runtime']  + runtime_ms,
    ['qmd_runtime'] + runtime_qmd
]
afs_runtimes = afstools.transposed(afs_runtimes)

output_filename = os.path.join('csv-files', f'afs_runtimes_M{migration_rate}_n{num_islands}_w{omega}.csv')
afstools.write_csv(afs_runtimes, output_filename, ',')