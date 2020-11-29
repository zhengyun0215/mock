import h5py
import numpy as np
import time
import multiprocessing as mp

print("Let's start!")
redshift = np.loadtxt('/home/yunzheng/mock/orphan/redshift.txt')

def vpeak(x):
    start = time.time()
    print('the redshift of snapshot %d is %s'%(x,redshift[x]))
    sub_file = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_0%s.hdf5'%x,'r')['Subhalos'][...]
    subid = sub_file['TrackId']
    vmax = sub_file['VmaxPhysical']
    birthsnap = sub_file['SnapshotIndexOfBirth']
    
    
    a = np.stack((subid,vmax,birthsnap),axis= -1)
    
    np.savetxt('/home/yunzheng/mock/color/data/vmax/snapshot_%s.dat'%x)
    
def multicore():
    pool = mp.Pool(processes = 64)
    res = pool.map(vpeak,range(100))

    pool.close()
    pool.join()
    print("bingo! yes!")
    
    
if __name__ == '__main__':
    multicore()
    
    
    
    
    