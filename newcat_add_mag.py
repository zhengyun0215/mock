import numpy as np

table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snap_92_new_with_zform.npy')

newmag_92 = np.loadtxt('/home/yunzheng/mock/abundance_new/data/newmag_92.txt')
sca_92 = np.loadtxt('/home/yunzheng/mock/abundance_new/data/scattermag/mag_92.txt')

subid = table[:,0]
vpeak = table[:,1]
pos_x = table[:,5]
pos_y = table[:,6]
pos_z = table[:,7]
v_x = table[:,8]
v_y = table[:,9]
v_z = table[:,10]
zform = table[:,11]


stag = np.argsort(vpeak)
subid = subid[stag]
vpeak = vpeak[stag]
pos_x = pos_x[stag]
pos_y = pos_y[stag]
pos_z = pos_z[stag]
v_x = v_x[stag]
v_y = v_y[stag]
v_z = v_z[stag]
zform = zform[stag]


stag_92 = np.argsort(-sca_92)
newmag = newmag_92[stag_92]

a = np.stack((subid,vpeak,pos_x,pos_y,pos_z,v_x,v_y,v_z,zform,newmag),axis= -1)
np.save('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new_withmag.npy',a)