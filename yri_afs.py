from numpy import loadtxt
import plotly.graph_objects as go
import afstools 
import sys

lines = loadtxt("FoldSFS_YRI.txt", delimiter ="\t", unpack = False)
afs = [line[1] for line in lines]
i = 0
len_x = 9
k = round(len(afs)/len_x)
new_afs = []
while i <= len(afs) - k:
	average = sum(afs[i:i+k])/round(k)
	new_afs.append(average)
	i += k 
if i < len(afs):
	new_afs.append(sum(afs[i:len(afs)])/len(afs[i:len(afs)]))

new_afs = afstools.normalized(new_afs)[0]
fig=go.Figure()
fig = afstools.visualize_afs(afs= new_afs, namefile='yri_afs_rescaled',fig=fig, nameline = 'yri_afs_rescaled')
fig = afstools.visualize_afs(afs= afstools.expected_panmictic_afs(10), namefile='yri_afs_rescaled',fig=fig, nameline = 'panmictic_afs')

islands = int(sys.argv[1])
migration = float(sys.argv[2])
sampling_type = sys.argv[3]
deme = float(sys.argv[4])
samples = afstools.sampling_scheme(total_samples = 10, type = sampling_type)
print(samples)
print(type(samples))
expected_nislands_afs = afstools.expected_nisland_afs(samples = samples, islands = islands, migration = migration , deme = deme, omega = 1.25)
fig = afstools.visualize_afs(show=True,save=True, afs= expected_nislands_afs, namefile='yri_nislands_afs',fig=fig, nameline = f'nislands_afs_{sampling_type}_{islands}i_M{migration}_deme{deme}')
