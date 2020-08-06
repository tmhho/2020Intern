import subprocess
import json
import csv

def read_csv(filename):
    return csv.reader(open(filename, encoding='utf-8-sig'), delimiter = ',')

def write_csv(table, filename, delimiter = '\t'):
    csv.writer(open(filename, 'w', newline=''), delimiter=delimiter).writerows(table)

def read_json(filename):
    with open(filename) as f:
        output_dict = json.load(f)
    
    return output_dict

def write_json(dictionary, filename):
	with open(filename, 'w') as json_file:
		json.dump(dictionary, json_file, indent = 4)
    
def datetime_tag():
	from time import strftime
	return strftime("%y%m%d-%H%M%S")

def transposed(table):
    return list(map(list, zip(*table)))    

def absolute_error(x, y):
    k = len(x)
    return sum(abs(x[i] - y[i]) for i in range(k))

def average_absolute_error(x,y):
    k = len(x)
    return sum(abs(x[i] - y[i]) for i in range(k))/(k-1)

def relative_error(x, y):
    k = len(x)
    return sum(abs(1 - x[i] / y[i]) for i in range(k))

def execute(cmd):
	popen = subprocess.Popen(cmd, stdout = subprocess.PIPE, universal_newlines = True)
	for stdout_line in iter(popen.stdout.readline, ""):
		yield stdout_line 
    
	popen.stdout.close()
	return_code = popen.wait()
	if return_code:
		raise subprocess.CalledProcessError(return_code, cmd)

def normalized(afs):
    total = int(sum(afs))
    return ([float(xi) / total for xi in afs], total)

def expected_panmictic_afs(samples):
    afs = [1 / xi for xi in range(1, samples)]
    total = sum(afs)
    afs = [xi / total for xi in afs]
    return afs

def expected_nisland_afs(samples, islands, migration, deme = 1.0, omega = 1.25):
    if len(samples) > islands:
        raise ValueError("Error: more sampling locations than islands!")
    elif len(samples) < islands:
        samples.extend([0] * (islands - len(samples)))

    qmd_cmd = ['./qmd', str(sum(samples)), str(islands), str(migration), str(deme)]
    qmd_cmd.extend(str(k) for k in samples)
    qmd_cmd.append(str(omega))
    
    line = next(execute(qmd_cmd)).strip()[1:-1]
    afs = [float(x) for x in line.split(',')]
    return afs

def sampling_scheme (total_samples, type):
    if total_samples % 2 != 0:
        raise 'Error: not an even number of samples'

    if type == 'half-half':
        from math import ceil, floor
        return [2 * ceil(total_samples / 4), 2 * floor(total_samples / 4)]
    
    if type == 'concentrated':
        return [total_samples]

    if type == 'spread':
        return [2] * int(total_samples / 2)
    
    raise f'Error: type argument not recognized: {type}'