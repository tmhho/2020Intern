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

reps = [
    500,
    1000,
    5000,
    10000,
    50000,
    100000,
    500000,
    1000000
]

samples_size = 6
mutation_rate = 0.1
num_islands = 10
migration_rate = float(sys.argv[1])
deme_size = 1.0
ms_commands = ['./ms {} {} -t {} -I {} {} 0 0 0 0 0 0 0 0 0 {}'.format(samples_size,nreps,mutation_rate, num_islands, samples_size, migration_rate) for nreps in reps]

file_names = ['ms_command_{}.ms'.format(nreps) for nreps in reps]


#EXPECTED AFS
omega = 1.25
qmd_cmd = ['./qmd', str(samples_size), str(num_islands), str(migration_rate), str(deme_size),str(samples_size),
'0', '0', '0', '0','0','0','0', '0', '0', str(omega)]
print(qmd_cmd)
for line in _execute(qmd_cmd):
    print(line)
    expected_afs = line.strip()[1:-1].split(',')
    expected_afs = [float(i) for i in expected_afs]

print(expected_afs)

#PANMICTIC AFS
panmictic_afs = [1 / i for i in range(1, samples_size)]
panmictic_afs = [x / sum(panmictic_afs) for x in panmictic_afs]
print(panmictic_afs)

abs_err = []
rel_err = []
#runtime = []

afs_table = [
    ['expected afs'] + expected_afs,
    ['panmictic_afs'] + panmictic_afs
]
i = 0
while i < len(reps):
    nrep = reps[i]
    filename = file_names[i]
    ms_command = ms_commands[i]
    print(ms_command)
    with open(filename, 'w') as f:
        f.writelines([ms_command])
    #mesure runtime
#    start_time = time.time()
    output_fn = parse_ms(filename, False)
#    runtime.append(time.time()-start_time)
    
    observed_afs = output_fn
    afs_table.append(
        ['observed {}'.format(nrep)] + observed_afs
    )

    abs_err.append(_absolute_error(observed_afs, expected_afs))
    rel_err.append(_relative_error(observed_afs, expected_afs))

    i += 1

afs_distances = [
    ['repetitions'] + reps,
    ['abs.error_{}'.format(migration_rate)]  + abs_err,
    ['rel.error_{}'.format(migration_rate)]  + rel_err,
#    ['runtime'   ]  + runtime
]

afs_distances = list(map(list,zip(*afs_distances)))
afs_table = list(map(list,zip(*afs_table)))
_write_csv(afs_table, 'afs_values_k=6_M={}_10i.csv'.format(migration_rate), ',')
_write_csv(afs_distances, 'afs_distances_k=6_M={}_10i.csv'.format(migration_rate), ',')
