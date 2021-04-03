import numpy as np

table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snap_92_new_with_zform.npy')

newmag_92 = np.loadtxt('/home/yunzheng/mock/abundance_new/data/newmag_92.txt')
sca_92 = np.loadtxt('/home/yunzheng/mock/abundance_new/data/scattermag/mag_92.txt')

subid = table[:,0]
vpeak = table[:,1]
mass = table[:,4]
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
mass  = mass[stag]
pos_x = pos_x[stag]
pos_y = pos_y[stag]
pos_z = pos_z[stag]
v_x = v_x[stag]
v_y = v_y[stag]
v_z = v_z[stag]
zform = zform[stag]


stag_92 = np.argsort(-sca_92)
newmag = newmag_92[stag_92]

color = np.load('/home/yunzheng/mock/color/data/zcdf_new/color_mul_normal.npy')


np.savez('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_final.npz',subid = subid,vpeak = vpeak,mass = mass,posx = pos_x,posy = pos_y,posz = pos_z,vx = v_x,vy = v_y,vz = v_z,zform = zform,mag = newmag,color = color)