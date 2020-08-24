import subprocess
import json
import csv
import ms2afs

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

def append_json(dictionary,filename):
	data = read_json(filename)
	data.update(dictionary)
	write_json(data, filename)
    
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

def visualize_afs(afs, namefile, nameline, fig, show = False ,save =False, has_title=False, title=None): 
	import plotly.graph_objects as go
	import plotly.io as pio
	import os
	# fig=go.Figure()
	fig.add_trace(go.Scatter(
    x=list(range(1, len(afs)+1)), y = afs,
    mode='lines+markers',
    line=dict(width=0.5),
    name = nameline))
	if has_title :
		fig.update_layout(title=title)
	if show :
		fig.show()
	if save :
		path_png = os.path.join('graphs',namefile +'_'+ afstools.datetime_tag() +'.png')
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


def fold(original_afs):
	afs_out = []
	l = len(original_afs)
	i = 0
	while i < l//2:
		afs_out.append(original_afs[i]+original_afs[l-i-1])
		i += 1
	if l % 2 == 1:
		afs_out.append(original_afs[l//2])
	return afs_out

def graphical_transform(original_afs): 
	afs_out = []
	n = len(original_afs)
	for i in range(1,n+1):
		afs_out.append((original_afs[i-1]*i*(2*n-i))/(2*n))
	return afs_out


# type of input is list of string
def simulated_nislands_size_inscreased_all_islands(yri_afs : list,num_islands:list, migration_rates:list, list_T:list, list_x:list, nreps:str) -> dict:
	import os
	data = {'model': 'Nislands-model with population size increased in all islands'} 
	for islands in num_islands:
		for T in list_T:
			for x in list_x:
				for M in migration_rates:
					ms_command = ['./ms', '216',nreps, '-t', '0.1','-I']
					samples = sampling_scheme(total_samples=216, type='concentrated')
					samples.extend([0] * (int(islands) - len(samples)))
					samples=[str(n) for n in samples]
					ms_command.extend([islands])
					ms_command.extend (samples)
					ms_command.extend([ M, '-eN', T, x])
					print(ms_command)
					afs = ms2afs._get_afs(ms_command, max_sites = 20000000, step = 1)
					afs = normalized(afs)[0]
					afs = fold(afs)
					data[f'{islands}islands_{T}T_{x}x_{M}M'] = afs
					filename = os.path.join('json-files', 'yri-afs_' + datetime_tag() + '_values.json')
					write_json(data,filename)
					distance = {'average_absolute_error': average_absolute_error(yri_afs,afs)}
					append_json(distance,filename)
	return data
# type of input is list of string
def simulated_nislands_size_inscreased_isolated_one_island(num_islands:list, migration_rates:list, list_T:list, list_x:list, nreps:str) -> dict:
	data2={'model': 'Nislands-model with population size increased in one island and its partial isolation' }
	for T in list_T:
		for x in list_x:
			for M in migration_rates:
				Tij = []
				for islands in num_islands:
					ms_command = ['./ms', '216','30000', '-t', '0.1','-I']
					samples = sampling_scheme(total_samples=216, type='concentrated')
					samples.extend([0] * (int(islands) - len(samples)))	
					samples=[str(n) for n in samples]
					ms_command.extend([islands])
					ms_command.extend (samples)
					ms_command.extend([M, '-en',T,'1',x])
					i_j_migration_rate = str(float(M)*float(x))
					for j in range(2, int(islands)+1):
						Tij.extend(['-em','T','1',str(j), i_j_migration_rate])
						Tij.extend(['-em','T',str(j),'1', i_j_migration_rate])
					ms_command += Tij
					print(ms_command)
					afs = ms2afs._get_afs(ms_command, max_sites = 200000, step = 1)
					afs = normalized(afs)[0]
					afs = fold(afs)
					data2[f'{islands}islands_{T}T_{x}x_{M}M'] = afs
	return data2