import subprocess
import csv

def read_csv(filename):
    return csv.reader(open(filename, encoding='utf-8-sig'), delimiter = ',')

def write_csv(table, filename, delimiter='\t'):
    csv.writer(open(filename, 'w', newline=''), delimiter=delimiter).writerows(table)

def transposed(table):
    return list(map(list, zip(*table)))    

def absolute_error(x, y):
    k = len(x)
    return sum(abs(x[i] - y[i]) for i in range(k))

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