import afstools
import ms2afs
import os

def get_sampled_afs(afs, reps):
    from random import choices

    samples = len(afs) + 1
    sampled_frequencies = choices(range(1, samples), weights = afs, k = reps)
    sampled_afs = [0] * (samples - 1)
    for xi in sampled_frequencies:
        sampled_afs[xi - 1] += 1
    
    return sampled_afs
    
def compare_panmictic(reps, samples, thetas):
    expected_afs = afstools.expected_panmictic_afs(samples)

    column = ['repetitions', 'sampling error']
    column.extend(f'ms error theta={theta}' for theta in thetas)

    afs_distances = [column]
    afs_table = [
        ['expected afs'] + expected_afs
    ]

    for rep in reps:
        print(f'starting {rep} segsites...')
    
        column = [rep]
        sampled_ms = get_sampled_afs(expected_afs, rep)
        sampled_ms = afstools.normalized(sampled_ms)[0]
        column.append(afstools.absolute_error(sampled_ms, expected_afs))

        for theta in thetas:
            print(f'    theta = {theta}')
            
            ms_afs = ms2afs.get_panmictic_afs(samples, theta, repetitions = 10 * rep,  max_sites = rep, step=100)
            ms_afs = afstools.normalized(ms_afs)[0]

            afs_table.extend([
                [f'ms snp={rep} t={theta}'] + ms_afs,
                [f'sampling snp={rep} t={theta}'] + sampled_ms
            ])

            column.append(afstools.absolute_error(ms_afs, expected_afs))
        
        afs_distances.append(column)
            
    afs_distances = afstools.transposed(afs_distances)
    afs_table = afstools.transposed(afs_table)
    datetime = afstools.datetime_tag()
    
    fn_tag = os.path.join('csv-files', f'afs_{datetime}_s{samples:d}_')
    afstools.write_csv(afs_table, fn_tag + 'values.csv', ',')
    afstools.write_csv(afs_distances, fn_tag + 'distances.csv', ',')

if __name__ == "__main__":
    reps = [
        500,
        1000,
        5000,
        10000,
        50000,
        # 100000,
        # 500000,
        # 1000000
    ]

    theta = [
        0.1,
        1,
        10,
    ]

    samples = 20

    compare_panmictic(reps, samples, theta)