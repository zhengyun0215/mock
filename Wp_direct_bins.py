
print('Strat!')

import numpy as np
# from Corrfunc.theory import *
# from astropy.coordinates import SkyCoord
# from scipy.spatial.transform import Rotation as R
# from astropy.cosmology import FlatLambdaCDM,z_at_value
# cosmo = FlatLambdaCDM(H0 = 100,Om0 = 0.268,Tcmb0=2.725)
# import matplotlib.pyplot as plt
# import astropy.units as u
# import multiprocessing as mp

from Corrfunc.theory.wp import wp
# from Corrfunc.theory import DDrppi
# from Corrfunc.utils import convert_rp_pi_counts_to_wp

table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snap_92_new_with_zform.npy')
newmag_92 = np.loadtxt('/home/yunzheng/mock/abundance_new/data/newmag_92.txt')
sca_92 = np.loadtxt('/home/yunzheng/mock/abundance_new/data/scattermag/mag_92.txt')

stag_92 = np.argsort(-sca_92)
newmag = newmag_92[stag_92]

vpeak = table[:,1]
pos_x = table[:,5]
pos_y = table[:,6]
pos_z = table[:,7]

stag = np.argsort(vpeak)
vpeak = vpeak[stag]
pos_x = pos_x[stag]
pos_y = pos_y[stag]
pos_z = pos_z[stag]

pos_x = pos_x / 1000
pos_y = pos_y / 1000
pos_z = pos_z / 1000

print('Load Sucessfully!')

def Mag_bin(i):
    
    print("Start! :)")
    
    m = i
    print('The Mag bin is %s'%m)
    
    temp = (newmag < m)
    mag_temp = newmag[temp]
    x_bin = pos_x[temp]
    y_bin = pos_y[temp]
    z_bin = pos_z[temp]
    print('The Mag bin is %s' % m)
    print("the max mag is %s" % (np.max(mag_temp)))
    print("the min mag is %s" % (np.min(mag_temp)))
    print("The max x is%s" % (np.max(x_bin)))
    print("The max y is%s" % (np.max(y_bin)))
    print("The max z is%s"%(np.max(z_bin)))

    aa=np.linspace(-2.,1.8,20)
    bins = 10.**aa
    results = wp(boxsize = 600,pimax=60,nthreads = 30,binfile = bins,X = x_bin,Y = y_bin,Z = z_bin,output_rpavg=True)
    
    np.savez('/home/yunzheng/mock/clustering/data/wp_direct/wp_bin_%s.npz'%i,rp = results['rpavg'],wp = results['wp'])
    
dat = np.array([18.5,19,19.5,20,20.5,21,21.5,22])
dat = -dat
print(dat)


if __name__ == '__main__':
    for i in (dat):
        print(i)
        Mag_bin(i)
    




