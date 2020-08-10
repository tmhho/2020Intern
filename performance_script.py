import afstools
import ms2afs
import time
import sys
import os
import numpy as np
nsegsites = 50000
k = [ 
    4,
    6,
    8,
    10,
    12,
    14,
    16,
    # 18
]

migration_rates = np.logspace(start=-2, stop = 1, num = 3)
type_sampling = sys.argv[2]
mutation_rate = 1.0

num_islands = int(sys.argv[1])
deme_size = 1.0
omega = 1.25


afs_runtimes = [['samples_size']+k]

for migration_rate in migration_rates:
  runtime_ms = []
  runtime_qmd = []
  for total_samples in k:
      sampling = afstools.sampling_scheme(total_samples,type_sampling)
      print('sampling:{}'.format(sampling))

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

  afs_runtimes.append([f'ms_runtime_M{migration_rate}']  + runtime_ms) 
  afs_runtimes.append([f'qmd_runtime_M{migration_rate}'] + runtime_qmd)

afs_runtimes = afstools.transposed(afs_runtimes)
datetime = afstools.datetime_tag()
output_filename = os.path.join('csv-files', f'{datetime}_runtimes_{num_islands}i_sampling={type_sampling}_omega={omega}_theta={mutation_rate}.csv')
afstools.write_csv(afs_runtimes, output_filename, ',')