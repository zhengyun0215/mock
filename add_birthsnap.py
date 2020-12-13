import numpy as np
import h5py
print("Let's start!")


sub_file = h5py.File('/home/cossim/CosmicGrowth/6610/subcat2/SubSnap_092.hdf5','r')['Subhalos'][...]
subid_0 = sub_file['TrackId']
birthsnap = sub_file['SnapshotIndexOfBirth']

subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_%s.txt'%92)
orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_%s/orphantable_final.npy'%92)



subid = np.concatenate((subhalo[:,0], orphan[:,0]))
subid = np.array(subid,dtype = int)
a = len(subid)
print('The length is %d'%a)

vpeak = np.concatenate((subhalo[:,4], orphan[:,4]))

vpeaksnap = np.concatenate((subhalo[:,5], orphan[:,5]))
vpeaksnap = np.array(vpeaksnap,dtype = 'int')

orp_mass = np.ones(len(orphan)) * 0.05541996
mass = np.concatenate((subhalo[:,6],orp_mass))

pos_x = np.concatenate((subhalo[:,7], orphan[:,6]))
pos_y = np.concatenate((subhalo[:,8], orphan[:,7]))
pos_z = np.concatenate((subhalo[:,9], orphan[:,8]))

v_x = np.concatenate((subhalo[:,10], orphan[:,9]))
v_y = np.concatenate((subhalo[:,11], orphan[:,10]))  
v_z = np.concatenate((subhalo[:,12], orphan[:,11]))                           

print(subid.shape)
print(vpeak.shape)
print(mass.shape)


birth = []
for i in range(len(subid)):
    birth.append(birthsnap[subid[i]])

print("the length of subid is %d"%(len(birth)))


a = np.stack((subid,vpeak,vpeaksnap,birth,mass,pos_x,pos_y,pos_z,v_x,v_y,v_z),axis= -1)
np.save('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new.npy',a)