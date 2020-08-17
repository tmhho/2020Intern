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

def sampling_scheme(total_samples, type, islands = 0):
    if total_samples % 2 != 0:
        raise 'Error: not an even number of samples'

    if type == 'half-half':
        from math import ceil, floor
        return [2 * ceil(total_samples / 4), 2 * floor(total_samples / 4)]
    
    if type == 'concentrated':
        return [total_samples]

    if type == 'spread':
        if islands == 0:
            return [2] * (total_samples // 2)
        else:
            sv = [0] * min(islands, total_samples // 2)
            i = 0
            for _ in range(total_samples // 2):
                sv[i] += 2
                if i == len(sv) - 1:
                    i = 0
                else:
                    i += 1
            
            return sv
    
    raise f'Error: type argument not recognized: {type}'

def visualize_afs(afs, namefile, nameline, fig, show = False ,save =False): 
	import plotly.graph_objects as go
	import plotly.io as pio
	import os
	# fig=go.Figure()
	fig.add_trace(go.Scatter(
    x=list(range(1, len(afs)+1)), y = afs,
    mode='lines+markers',
    line=dict(width=0.5),
    name = nameline))
	if show :
		fig.show()
	if save :
		path_png = os.path.join('graphs',namefile +'_'+ datetime_tag() +'.png')
		pio.write_image(fig , path_png, 'png')
	return fig



def subsample(original_afs, subsample_size):
	from math import floor
	k = (10 * len(original_afs))/subsample_size 
	# print('k   ', k)
	list_rest = [10]*len(original_afs)
	afs_out = [] 
	i = 0
	while len(afs_out) < subsample_size:
		value = 0
		used = 0
		step = 0
		# print('we are at i : ', i)
		while used < k:
			if k - used >= list_rest[i]:
				value += list_rest[i]*original_afs[i]/10.0
				used += list_rest[i]
				step = list_rest[i]	
				list_rest[i] = 0
				i += 1
			else :
				value += (k - used)*original_afs[i]/10.0
				step = k - used
				list_rest[i] =  list_rest[i] - step

				used = k   
			# print('step used: ', step)
			# print(list_rest)	
		afs_out.append(value)

		# print('afs out is: ', afs_out)
		
	return afs_out