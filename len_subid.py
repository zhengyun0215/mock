import numpy as np
import h5py
import time
import multiprocessing as mp

print("Let's start!")


snaplen = []


def lenth(x):
    start = time.time()
    print('the snapshot number is %d'%x)
    
    sub_file_id = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_%03d.hdf5'%x,'r')['Subhalos']['TrackId']
    
    a = len(sub_file_id)
    
    end = time.time()
    print("time spent : %s minutes"%((end - start)/60))
    return a
    
    
    
def multicore():
    pool = mp.Pool(processes = 64)
    res = pool.map(lenth,range(100))
    res = np.array(res)
    np.savetxt('/home/yunzheng/mock/color/data/len_all.txt',res)
    pool.close()
    pool.join()
    print("bingo! yes!")
    
    
if __name__ == '__main__':
    multicore()
    