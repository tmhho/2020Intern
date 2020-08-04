from csv import writer

import afstools

import os
import subprocess
import argparse

if os.name == 'nt':
	_ms_program = './ms.exe'
else:
	_ms_program = './ms'

def _get_afs(ms_command, max_sites = 0, step = 1):
	from math import ceil

	k = int(ms_command[1])
	block_reading = False
	block_progress = 0
	total_sites = 0

	if max_sites < 1:
		max_sites = float('inf')
	
	afs = [0] * (k - 1)
	ms_output = afstools.execute(ms_command)
	for line in ms_output:
		if block_reading:
			block_progress += 1
			
			if block_progress > k + 1:
				block_reading = False
				for site_count in site_counts:
					afs[site_count - 1] += 1
				
				if total_sites == max_sites:
					break
			
			elif block_progress > 1:
				for i in range(sampled_sites):
					if line[i * step] == '1':
						site_counts[i] += 1
			continue

		if line[0] == 's': # segsites: <sites>
			sites = int(line.split()[1])
			if sites > 0:
				block_reading = True
				block_progress = 0
				sampled_sites = ceil(sites / step)
				sampled_sites = min(sampled_sites, max_sites - total_sites)
				total_sites += sampled_sites
				site_counts = [0] * sampled_sites
	
	if block_reading:
		for site_count in site_counts:
			afs[site_count - 1] += 1

	try:
		while True:
			next(ms_output)
	except StopIteration:
		pass	

	return afs

def get_panmictic_afs(samples, theta, repetitions, max_sites = 0, step = 1):
	ms_command = [_ms_program, str(samples), str(repetitions), '-t', str(theta)]
	return _get_afs(ms_command, max_sites, step)

def get_nisland_afs(islands, migration, samples, theta, repetitions, max_sites = 0, step = 1):
	if len(samples) > islands:
		raise ValueError("Error: more sampling locations than islands!")
	elif len(samples) < islands:
		samples.extend([0] * (islands - len(samples)))
	
	ms_command = [_ms_program, str(sum(samples)), str(repetitions), '-t', str(theta), '-I', str(islands)]
	ms_command.extend(str(k) for k in samples)
	ms_command.append(str(migration))

	return _get_afs(ms_command, max_sites, step)

def parse_ms(filename, absolute, max_sites = 0, step = 1):
	with open(filename, 'r') as f:
		ms_command = f.readline().split()

	afs = _get_afs(ms_command, max_sites, step)
	if not absolute:
		afs = [xi / total_sites for xi in afs]

	return afs

def _get_source_filenames(data_source):
	if path.isfile(data_source):
		return [data_source]

	if not path.isdir(data_source):
		raise ValueError('Invalid data source string')
	
	from glob import glob
	pattern = path.join(data_source, '*.ms')
	file_list = glob(pattern)	
	file_list.sort()

	return file_list

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('path', help = 'Path to file with an ms command or a directory of such files')
	parser.add_argument('-a', '--absolute', help = 'Specify that the output should be in absolute mutations count (unscaled)', action = "store_true")
	parser.add_argument('-s', '--step', help = 'Take one from every `step` segsites', type = int, default = 1)
	args = parser.parse_args()

	filenames = _get_source_filenames(args.path)
	for filename in filenames:
		afs = parse_ms(filename, args.absolute, step=args.step)
		outfilename = path.splitext(filename)[0] + '.csv'
		writer(open(outfilename, 'w', newline='')).writerows([afs])
		print(f'File {path.basename(outfilename)} generated successfully!')