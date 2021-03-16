
print('Strat!')

import numpy as np

from Corrfunc.theory.wp import wp

print("Let's start!!!!!!!!")
table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new_withmag.npy')
posx = table[:, 2] / 1000  #########change into Mpc/h
posy = table[:, 3] / 1000
posz = table[:, 4] / 1000
mag = table[:, 9]

print('Load Sucessfully!')

##########  box参数  ##########
boxsize0 = 600
pimax0 = 60
# nthreads0 = 40
aa = np.linspace(-2., 1.8, 20)
bins0 = 10. ** aa
nrpbins0 = len(bins0) - 1
print('Load Sucessfully!')

def Mag_bin(i):
    
    print("Start! :)")
    
    m = i
    print('The Mag bin is %s'%m)
    
    temp = (mag < m)
    mag_temp = mag[temp]
    x_bin = posx[temp]
    y_bin = posy[temp]
    z_bin = posz[temp]
    
    print('The Mag bin is %s' % m)
    print("the max mag is %s" % (np.max(mag_temp)))
    print("the min mag is %s" % (np.min(mag_temp)))
    print("The max x is%s" % (np.max(x_bin)))
    print("The max y is%s" % (np.max(y_bin)))
    print("The max z is%s"%(np.max(z_bin)))



    aa=np.linspace(-2.,1.8,20)
    bins = 10.**aa
    results = wp(boxsize = 600,pimax=60,nthreads = 30,binfile = bins0,X = x_bin,Y = y_bin,Z = z_bin,output_rpavg=True)
    
    np.savez('/home/yunzheng/mock/clustering/data/wp_direct/wp2_bin_%s.npz'%i,rp = results['rpavg'],wp = results['wp'])
    
dat = np.array([18.5,19,19.5,20,20.5,21,21.5,22])
dat = -dat
print(dat)


if __name__ == '__main__':
    for i in (dat):
        print(i)
        Mag_bin(i)
    




