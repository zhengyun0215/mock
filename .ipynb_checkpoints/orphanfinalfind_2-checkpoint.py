import h5py
import numpy as np
import time
import multiprocessing as mp


def selection(x):
    print("Start! :)")
    start = time.time()
    print('The snapshot id is %s'%x)
    orpnum = np.loadtxt('/home/yunzheng/mock/orphan_new/orphantabel_new/snapshot_%s/fsnapnum.txt'%x)
    vel_ratio = np.load('/home/yunzheng/mock/orphan/vel_ratio.npy')
    t_infall = np.loadtxt('/home/yunzheng/mock/orphan_new/t_infall_new/t_infall_%s.txt'%x)


    orpnum = np.array(orpnum,dtype = int)
    constant = (0.94*(0.51**0.6)+0.6)/0.86
    print(constant)

    orphantable_final = []
    orphan_final = [[]for _ in range(100)]
    fsnap_final = np.zeros(100)


    m = 0
    for i in range(100):

        if orpnum[i] > 0:
            j = 0
            Nsnap = i
            print("******Snapshot******:%d"%Nsnap)
            #读取Nsnap这个snapshot的相关文件
            sub_file = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_%03d.hdf5'%(i),'r')['Subhalos'][...] 
            sub_file_1 = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_%03d.hdf5'%(i+1),'r')['Subhalos'][...] 
            cen_find = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_%03d.hdf5'%(i+1),'r')['Membership/GroupedTrackIds'][...] 
            host_file = np.loadtxt('/home/yunzheng/mock/orphan/halosize/hosthalo_%s.dat'%(i))
            orphantable = np.load('/home/yunzheng/mock/orphan_new/orphantabel_new/snapshot_%s/orphantable_savetest_%s.npy'%(x,i))

            for q in range(orpnum[Nsnap]):

                subhaloid = np.array(orphantable[q][0],dtype = int)
                subhostid = sub_file[subhaloid]['HostHaloId']

                if subhostid!=-1:
                    Msat = host_file[subhostid][1]

                    if Msat > 0:
                        hosthaloid_1 = sub_file_1[subhaloid]['HostHaloId']
                        cenid = cen_find[hosthaloid_1][0]
                        cenhostid = sub_file[cenid]['HostHaloId']

                        if cenhostid != -1:
                            Mcen = host_file[cenhostid][1]
                            mass_ratio = Mcen / Msat

                            t = constant * vel_ratio[Nsnap] * mass_ratio / (np.log(1+mass_ratio))

                            t_in = t_infall[Nsnap]
                            if t_in <= t:
                                j = j +1
                                m = m +1
                                fsnap_final[Nsnap] = fsnap_final[Nsnap] + 1
                                orphantable_final.append(orphantable[q])
                                orphan_final[Nsnap].append(orphantable[q])

            np.save('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_%s/snap_%d.npy'%(x,i),orphan_final[Nsnap])
            print("the orphan number :%d"%j)
            print("For each snapshot :%d"%(fsnap_final[Nsnap]))
    print("the total number :%d"%m)
    print("the total number :%d"%(np.sum(fsnap_final)))

    end = time.time()
    print("time spent : %s minutes"%((end - start)/60))

    np.save('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_%s/orphantable_final.npy'%(x),orphantable_final)
    np.savetxt('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_%s/final_orpnum.txt'%(x),fsnap_final)

    
dat = np.array([84,85,86,87,88,89,91,92,94,95,97,99])

def multicore():
    pool = mp.Pool(processes = 36)
    res = pool.map(selection,dat)
    
    
    pool.close()
    pool.join()
    print("bingo! yes!")
    
    
if __name__ == '__main__':
    multicore()
    

