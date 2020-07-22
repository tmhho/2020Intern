from ms2afs import parse_ms
from ms2afs import _execute
import csv
import time
import sys

def _read_csv(filename):
    return csv.reader(open(filename, encoding='utf-8-sig'), delimiter = ',')

def _write_csv(table, filename, delimiter='\t'):
    csv.writer(open(filename, 'w', newline=''), delimiter=delimiter).writerows(table)

def _absolute_error(x, y):
    k = len(x)
    return sum(abs(x[i] - y[i]) for i in range(k))

def _relative_error(x, y):
    k = len(x)
    return sum(abs(1 - x[i] / y[i]) for i in range(k))

nreps = 1000000

k = [ 2,
      4,
      6,
      8,
      10,
      12,
      14,
      # 16,
      # 18
      ]
mutation_rate = 0.1
num_islands = 10
migration_rate = float(sys.argv[1])

deme_size=1.0
ms_commands = ['./ms {} {} -t {} -I {} {} 0 0 0 0 0 0 0 0 0 {}'.format(samples_size,nreps, mutation_rate,num_islands, 
    samples_size,migration_rate) for samples_size in k]

file_names = ['ms_command_{}.ms'.format(samples_size) for samples_size in k]

#---------------------------------

runtime = []
runtime_qmd = []

i = 0

deme_size = 1.0
omega = 1.25
while i < len(k):
    samples_size = k[i]
    filename = file_names[i]
    ms_command = ms_commands[i]
    print(ms_command)
    with open(filename, 'w') as f:
        f.writelines([ms_command])
        
    #mesure runtime
    start_time = time.time()
    output_fn = parse_ms(filename, False)
    runtime.append(time.time()-start_time)
    
    start_time1=time.time()
    qmd_cmd = ['./qmd', str(samples_size), str(num_islands), str(migration_rate), str(deme_size),str(samples_size),
    '0', '0', '0', '0','0','0','0', '0', '0', str(omega)]
    for line in _execute(qmd_cmd):
        expected_afs = line.strip()[1:-1].split(',')
    runtime_qmd.append(time.time()-start_time1)

    i += 1

afs_distances = [
    ['samples_size'] + k,
    ['ms_runtime_M={}'.format(migration_rate) ]  + runtime,
    ['qmd_runtime_M={}'.format(migration_rate)] + runtime_qmd
]
afs_distances = list(map(list,zip(*afs_distances)))
# _write_csv(afs_table, 'afs_values_M=10_nislands=10.csv', ',')
_write_csv(afs_distances, 'afs_distances_M={}_10i.csv'.format(migration_rate), ',')
