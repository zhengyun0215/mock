import numpy as np
import h5py
import multiprocessing as mp

########   读文件   #########
table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_final.npy.npz')
print(table.files)
subid = table['subid']
posx = table['posx'] / 1000
posy = table['posy'] / 1000
posz = table['posz'] / 1000
vx = table['vx']
vy = table['vy']
vz = table['vz']
mag = table['mag']
color = table['color']



sub_file = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_%03d.hdf5' % (92), 'r')['Subhalos'][...]
last_iso = sub_file['SnapshotIndexOfLastIsolation']



########  并行读取Mvir  ########
def read(i):
    if i % 1000000 == 0:
        print("subhalo id is %d" % i)

    ############  读取subhalo id 找到相应的last isolation snapshot  ########
    subhaloid = int(subid[i])
    snap = last_iso[subhaloid]


    ############  读取subhalo last isolation snapshot 文件  找到相应的hosthalo id  ########
    subhaolo_iso_file = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_%03d.hdf5' % (snap), 'r')['Subhalos'][...]
    host_file = np.loadtxt('/home/yunzheng/mock/orphan/halosize/hosthalo_%s.dat' % (snap))
    hosthaloid = subhaolo_iso_file[subhaloid]['HostHaloId']
    Mvir = host_file[hosthaloid][1]
    subhaolo_iso_file.close()
    return (Mvir)


def multicore():
    pool = mp.Pool(processes= 20)
    res = pool.map(read,range(26241654))
    np.savez("/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_final_withmass.npz",subid = subid,posx = posx,posy = posy,posz = posz,vx = vx,vy = vy,vz = vz,mag = mag,color = color,mvir = res)
    pool.close()
    pool.join()
    print("Bingo!Yes!")
    
    
    
if __name__ == '__main__':
    multicore()



