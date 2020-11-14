import numpy as np
import os
import h5py
import time
import multiprocessing as mp

def read(x):
    print("Start! :)")
    start = time.time()
    print('The snapshot id is %s'%x)
    sub_file = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_0%s.hdf5'%x,'r')['Subhalos'][...]
    subid = sub_file['TrackId']
    subp = sub_file['Nbound']
    rank = sub_file['Rank']
    depth = sub_file['Depth']
    sinkid = sub_file['SinkTrackId']
    masspeak = sub_file['LastMaxMass']
    snap_masspeak = sub_file['SnapshotIndexOfLastMaxMass']
    last_iso =sub_file['SnapshotIndexOfLastIsolation']
    Vmaxpeak = sub_file['LastMaxVmaxPhysical']
    snap_vmaxpeak = sub_file['SnapshotIndexOfLastMaxVmax']
    position = sub_file['ComovingMostBoundPosition']
    velocity = sub_file['PhysicalMostBoundVelocity']
    
    
    orphantable = [[]for _ in range(100)]
    j = 0
    fsnapnum = np.zeros(100)
    
    
    for i in range(len(subid)):
        if i%1000000 == 0:
            print("subhalo id is %d"%i)
        if subp[i] == 1 and rank[i] > 0 and depth[i] > 0 and sinkid[i] < 0 and masspeak[i] > 2.771:
            j = j+1
            fsnapnum[last_iso[i]] = fsnapnum[last_iso[i]]+1

            # save info into file;        
            sub_info = np.array((i, masspeak[i], snap_masspeak[i] , last_iso[i] , Vmaxpeak[i], snap_vmaxpeak[i]))
            info_3d = np.append(position[i], velocity[i])
            sub_info_all = np.append(sub_info, info_3d)

            # i, masspeak[i], last_99[i], Vmaxpeak[i], position[i][x,y,x], velocity[i][x,y,z]
            orphantable[last_iso[i]].append(sub_info_all)
            

    for i in range(100):
        np.save('/home/yunzheng/mock/orphan_new/orphantabel_new/snapshot_%d/orphantable_savetest_%d.npy'%(x,i),orphantable[i])


    end = time.time()
    print("time spent : %s minutes"%((end - start)/60))


    print("the orphan number :%d"%j)
    print("For total snapshot :%d"%(np.sum(fsnapnum)))
    
    np.savetxt('/home/yunzheng/mock/orphan_new/orphantabel_new/snapshot_%d/fsnapnum.txt'%x,fsnapnum)    
    

dat = np.array([84,85,86,87,88,89,91,92,94,95,97,99])

def multicore():
    pool = mp.Pool(processes = 36)
    res = pool.map(read,dat)
    #     np.savetxt('/home/yunzheng/mock/orphan_new/test_%d.txt'%i,res)
    #     print(res)
    pool.close()
    pool.join()
    print("bingo! yes!")
    
    
if __name__ == '__main__':
    multicore()
    
