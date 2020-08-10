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

result_dir ='csv-files'
# migration_rates = np.logspace(start=-2, stop = 1, num = 3)
migration_rates = [0.1,1.0,10.0]
num_islands = int(sys.argv[1])
sampling_type = sys.argv[2]
mutation_rate = 1.0
deme_size = 1.0
omega = 1.25


afs_runtimes = [['samples_size']+k]

for migration_rate in migration_rates:
  runtime_ms = []
  runtime_qmd = []
  for total_samples in k:
      sampling = afstools.sampling_scheme(total_samples,sampling_type)
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
datetime = afstools.datetime_tag()
afs_runtimes = afstools.transposed(afs_runtimes)
basename = f'afs_performance_nislands_{datetime}_'

name_afs_runtime = os.path.join(result_dir, basename + '.csv')
afstools.write_csv(afs_runtimes, name_afs_runtime, ',')
afs_settings={
  "basename" : basename,
  "runtime filename": name_afs_runtime,
  "number of segsites" : nsegsites,
  "sampling type" : sampling_type,
  "number of islands" : num_islands,
  "migration rates" : migration_rates,
  "theta" : mutation_rate,
  "omega" : omega,
  "list of total samples" : k
}
name_afs_settings = os.path.joint(result_dir, basename + 'settings.json')
afstools.write_json(afs_settings, name_afs_settings)