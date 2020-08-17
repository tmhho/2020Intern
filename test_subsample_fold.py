from afstools import subsample
from afstools import fold
afs=[9,1,2,3,4,5,6,7,1]
print(afs)
afs = subsample(afs,6)
print('subsampled afs: ', afs)
afs = fold(afs)
print('folded afs: ', afs)