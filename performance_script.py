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

migration_rates = [
    0.1,
    1.0,
    10.0
]

def sampling_scheme (total_samples, type):
    if total_samples % 2 != 0:
        raise "Error: not an even number of samples!"

    if type == 'half-half':
        from math import ceil, floor
        return [2 * ceil(total_samples / 4), 2 * floor(total_samples / 4)]

    if type == 'concentrated':
        return [total_samples]

    if type == 'spread':
        return [2] * int(total_samples / 2)

    raise "Error: Unknown sampling type!"

type_sampling = sys.argv[1]
mutation_rate = 0.1
num_islands = 10
deme_size = 1.0
omega = 1.25

runtime_ms = []
runtime_qmd = []
afs_runtimes = [['samples_size'] + k]
for migration_rate in migration_rates:
  for total_samples in k:
      sampling = sampling_scheme(total_samples, type_sampling)
      print(f'sampling:', sampling)

      # measure ms runtime
      start_time = time.time()
      ms_afs = ms2afs.get_nisland_afs(num_islands, migration_rate, sampling, 
          mutation_rate, 10 * nreps, nreps)
      runtime_ms.append(time.time() - start_time)

      # measure qmd runtime
      start_time = time.time()
      qmd_afs = afstools.expected_nisland_afs(sampling, num_islands, migration_rate, deme_size, omega)
      runtime_qmd.append(time.time() - start_time)

  afs_runtimes.append([f'ms_runtime_M{migration_rate}']  + runtime_ms) 
  afs_runtimes.append([f'qmd_runtime_M{migration_rate}'] + runtime_qmd)

afs_runtimes = afstools.transposed(afs_runtimes)

output_filename = os.path.join('csv-files', f'afs_runtimes_n={num_islands}_w={omega}_sampling={type_sampling}.csv')
afstools.write_csv(afs_runtimes, output_filename, ',')