from numpy import loadtxt
import plotly.graph_objects as go
import afstools 
import sys
import ms2afs

lines = loadtxt("FoldSFS_YRI.txt", delimiter ="\t", unpack = False)
afs = [line[1] for line in lines]
i = 0
subsampled_yri_afs = afstools.subsample(afs,6)
yri_afs = afstools.normalized(subsampled_yri_afs)[0]

fig=go.Figure()
fig = afstools.visualize_afs(afs= yri_afs, namefile='yri_afs',fig=fig, nameline = 'yri_afs')

expected_panmictic_afs = afstools.expected_panmictic_afs(12)
folded_expected_panmictic_afs = afstools.fold(expected_panmictic_afs)
fig = afstools.visualize_afs(afs= folded_expected_panmictic_afs, namefile='yri_afs',fig=fig, nameline = 'panmictic_afs')

islands = int(sys.argv[1])
migration = float(sys.argv[2])
sampling_type = sys.argv[3]
deme = float(sys.argv[4])
samples = afstools.sampling_scheme(total_samples = 12, type = sampling_type)

qmd_nislands_afs = afstools.expected_nisland_afs(samples = samples, islands = islands, migration = migration , deme = deme, omega = 1.25)
folded_qmd_afs = afstools.fold(qmd_nislands_afs)
fig = afstools.visualize_afs(show=False,save=False, 
	afs= folded_qmd_afs, 
	namefile='yri_nislands_afs',
	fig=fig, 
	nameline = f'qmd_nislands_afs_{sampling_type}_{islands}i_M{migration}_deme{deme}')

num_segsites = 50000
nreps = 10*num_segsites
mutation_rate = 0.1
ms_nislands_afs = ms2afs.get_nisland_afs(
                islands = islands, 
                migration = migration,
                samples = samples, 
                theta = mutation_rate, 
                repetitions = nreps, 
                max_sites = num_segsites, 
                step = 100
            )
ms_nislands_afs = afstools.normalized(ms_nislands_afs)[0]
folded_ms_afs = afstools.fold(ms_nislands_afs)
fig = afstools.visualize_afs(show=True,save=True, 
	afs= folded_ms_afs, 
	namefile='yri_nislands_afs',
	fig=fig, 
	nameline = f'ms_nislands_afs_{sampling_type}_{islands}i_M{migration}_{num_segsites}segsites_theta{mutation_rate}')