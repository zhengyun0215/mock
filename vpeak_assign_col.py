import h5py
import numpy as np
import time
import multiprocessing as mp

print("Let's start!")
redshift = np.loadtxt('/home/yunzheng/mock/orphan/redshift.txt')

def vpeak(x):
    start = time.time()
    print('the redshift of snapshot %d is %s'%(x,redshift[x]))
    sub_file = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_%03d.hdf5'%x,'r')['Subhalos'][...]
    subid = sub_file['TrackId']
    vmax = sub_file['VmaxPhysical']
    birthsnap = sub_file['SnapshotIndexOfBirth']
    
    print("the length of subid is %d"%(len(subid)))
    a = np.stack((subid,vmax,birthsnap),axis= -1)
    
    np.save('/home/yunzheng/mock/color/data/vmax/snapshot_%s.npy'%x,a)
    end = time.time()
    print("time spent : %s minutes"%((end - start)/60))
    
def multicore():
    pool = mp.Pool(processes = 50)
    res = pool.map(vpeak,range(100))

    pool.close()
    pool.join()
    print("bingo! yes!")
    
    
if __name__ == '__main__':
    multicore()
    
    
    
    
    