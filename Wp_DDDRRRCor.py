import numpy as np
from astropy.coordinates import SkyCoord
from scipy.spatial.transform import Rotation as R
# from astropy.cosmology import FlatLambdaCDM,z_at_value
# cosmo = FlatLambdaCDM(H0 = 100,Om0 = 0.268,Tcmb0=2.725)
import astropy.units as u
import multiprocessing as mp
# from Corrfunc.theory import *
# from Corrfunc.theory.wp import wp
from Corrfunc.theory import DDrppi
from Corrfunc.utils import convert_rp_pi_counts_to_wp

table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new_withmag.npy')
posx = table[:,2] / 1000
posy = table[:,3] / 1000
posz = table[:,4] / 1000
mag = table[:,9]

##########  box参数  ##########
boxsize0 = 600
pimax0 = 60
nthreads0 = 40
aa = np.linspace(-2., 1.8, 20)
bins0 = 10. ** aa
nrpbins0 = len(bins0) - 1
print('Load Sucessfully!')

##########  并行分mag bin计算wp  ############
def Mag_bin(i):
    print("Start! :)")

    m = -i
    print('The Mag bin is %s' % m)

    temp = (mag < m)
    x_bin = posx[temp]
    y_bin = posy[temp]
    z_bin = posz[temp]

    N = len(x_bin)
    rand_N = 3 * N
    seed = 42
    np.random.seed(seed)
    rand_X = np.random.uniform(0, boxsize0, rand_N)
    rand_Y = np.random.uniform(0, boxsize0, rand_N)
    rand_Z = np.random.uniform(0, boxsize0, rand_N)

    DDn = DDrppi(autocorr = 1,nthreads = nthreads0,pimax = pimax0,binfile = bins0,X1 = x_bin,Y1 = y_bin, Z1 = z_bin)
    DRn = DDrppi(autocorr = 0,nthreads = nthreads0,pimax = pimax0,binfile = bins0,X1 = x_bin,Y1 = y_bin, Z1 = z_bin,X2 = rand_X,Y2 = rand_Y,Z2 = rand_Z)
    RRn = DDrppi(autocorr = 1,nthreads = nthreads0,pimax = pimax0,binfile = bins0,X1 = rand_X,Y1 = rand_Y, Z1 = rand_Z)


    wp = convert_rp_pi_counts_to_wp(N,N,rand_N,rand_N,DDn,DRn,DRn,RRn,nrpbins0,pimax0,estimator=u'LS')
    aa10=10**(aa+0.1)
    rrp=aa10[0:19]
    wp_result=np.stack((wp,rrp),axis=-1)

    np.save('/home/yunzheng/mock/clustering/data/wp_direct/wp_bin_%s.npy'%i, wp_result)


dat = np.array([18.5,19,19.5,20,20.5,21,21.5,22])
pool = mp.Pool(processes = 64)
res = pool.map(Mag_bin,dat)
pool.close()
pool.join()
print("bingo! yes!")

