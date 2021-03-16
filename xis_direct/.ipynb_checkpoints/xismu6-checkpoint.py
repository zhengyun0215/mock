import numpy as np
from nbodykit import transform
from astropy.cosmology import FlatLambdaCDM,z_at_value
from Corrfunc.theory import DDsmu
from scipy import integrate
import time
from astropy import units
import astropy.units as u
from astropy.constants import c
from Corrfunc.utils import convert_3d_counts_to_cf


cosmo = FlatLambdaCDM(H0=71, Om0=0.268, Tcmb0=2.725)
h = cosmo.h
print("The cosmology parameter is %d"%h)

print("Let's start!!!!!!!!")
table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new_withmag.npy')
posx = table[:, 2] / 1000  #########change into Mpc/h
posy = table[:, 3] / 1000
posz = table[:, 4] / 1000
vx = table[:, 5]
vy = table[:, 6]
vz = table[:, 7]
mag = table[:, 9]

print("The position has been loaded !!!!!")

#############  add redshift distortion  ##############
redshift = np.linspace(0,0.6,100000)
cd = cosmo.comoving_distance(redshift) * h   ###############Mpc/h
print("The length of the cd:",len(cd))
vpec = vz
cv = c.to('km/s').value
print("The light speed is:",cv)

z_cos = np.interp(posz,cd.value,redshift)
z_obs = z_cos + vpec / cv * (1 + z_cos)
sz = np.interp(z_obs,redshift,cd.value)
print("The redshift finished!!!!!")

##########  box参数  ##########
boxsize0 = 600
nthreads0 = 30
aa = np.linspace(-2., 1.8, 20)
bins0 = 10. ** aa
nsbins0 = len(bins0) - 1
nmubins = 100
print('Parameter Load Sucessfully!')


def Mag_bin(i):
    print("Start! :)")

    m = -i

    temp = (mag < m)
    mag_temp = mag[temp]
    xnew_temp = posx[temp]
    ynew_temp = posy[temp]
    znew_temp = sz[temp]
    #     comd_temp = comd[temp]
    print('The Mag bin is %s' % m)
    print("the max mag is %s" % (np.max(mag_temp)))
    print("the min mag is %s" % (np.min(mag_temp)))
    print("The max x is%s" % (np.max(xnew_temp)))
    print("The max y is%s" % (np.max(ynew_temp)))
    print("The max z is%s"%(np.max(znew_temp)))

    ztem = (znew_temp > boxsize0)
    znew_temp[ztem] -= boxsize0
    print("The max z is%s"%(np.max(znew_temp)))

    N = len(xnew_temp)

    if (m < -20.5):
        rand_N = 50 * N
        print('The Mag bin is %s' % m)
        print('The galaxy number is', N)
        print('The random number is', rand_N)
    elif (m < -20):
        rand_N = 40 * N
        print('The Mag bin is %s' % m)
        print('The galaxy number is', N)
        print('The random number is', rand_N)
    else:
        rand_N = 10 * N
        print('The Mag bin is %s' % m)
        print("The galaxy number is", N)
        print('The random number is', rand_N)

    print('The Mag bin is %s' % m)
    print("The length of this bin is", len(ynew_temp))
    print("The correlation function starts!!!!!!!")

    seed = 42
    np.random.seed(seed)
    rand_X = np.random.uniform(0, boxsize0, rand_N)
    rand_Y = np.random.uniform(0, boxsize0, rand_N)
    rand_Z = np.random.uniform(0, boxsize0, rand_N)
    #     pos_r = np.stack((rand_X, rand_Y, rand_Z), axis=-1)
    print('The random sample is sucessful!')
    print('The number of random sample is :', rand_N)

    ###########  pair count  #############

    mu_max = 1.0

    autocorr = 1
    DDn = DDsmu(autocorr, nthreads0, bins0, mu_max, nmubins, xnew_temp, ynew_temp, znew_temp, periodic=True,
                boxsize=boxsize0, output_savg=True)
    print("DDn finish!!!!!")

    autocorr = 0
    DRn = DDsmu(autocorr, nthreads0, bins0, mu_max, nmubins, xnew_temp, ynew_temp, znew_temp, periodic=True, X2=rand_X,
                Y2=rand_Y, Z2=rand_Z, boxsize=boxsize0)
    print("DRn finish!!!!!!!!")

    autocorr = 1
    RRn = DDsmu(autocorr, nthreads0, bins0, mu_max, nmubins, rand_X, rand_Y, rand_Z, periodic=True, boxsize=boxsize0)
    print("RRn finish!!!!!!!!!")

    # DDcounts = DDn['npairs']
    # DRcounts = DRn['npairs']
    # RRcounts = RRn['npairs']

    #############   存文件，含关键字   #############
    #     np.savez('/home/yunzheng/mock/clustering/data/xi/xi_circle/paircounts4_%s.npz'% i, N=N, rand_N=rand_N, DD=DDcounts, DR=DRcounts,RR=RRcounts, DDsavg=DDs)
    print("The counts has finished!!!")

    #############  利用LS估算公式求xi  ############
    ratio = rand_N / N
    print("Ratio is ", ratio)
    # xi2d = ratio ** 2 * DDcounts / RRcounts - 2 * ratio * DRcounts / RRcounts + 1

    #############  对mu积分得到xi 0阶  #############
    delta_mu = 1.0 / nmubins
    mu_p = np.linspace(0.01, 1.0, nmubins) - 0.5 * delta_mu

    #############   得到每一个s0 对应的xi(s0,mu)  ################
    # xi_smu = xi2d.reshape(-1, nmubins)
    # xi0 = integrate.trapz(xi_smu, mu_p)
    # print("The shape of xi0 is:", xi0.shape)

    savg = np.mean(DDn['savg'].reshape(-1, nmubins), axis=1)
    print("The shape of savg is:", savg.shape)

    ###############  对比直接用corrfun计算  ###################
    xi = convert_3d_counts_to_cf(N, N, rand_N, rand_N, DDn, DRn, DRn, RRn, estimator=u'LS')
    np.savez('/home/yunzheng/mock/clustering/data/xis_direct/xi_%s.npz' % i, s=savg, xi=xi)
    print('The correlation function has finished!!!!!')

    xi_cor_smu = xi.reshape(-1, nmubins)
    xi0_cor = integrate.trapz(xi_cor_smu, mu_p)
    np.savez('/home/yunzheng/mock/clustering/data/xis_direct/ximonopole_%s.npz' % i, s=savg, xi0=xi0_cor)


# dat = np.array([18.5, 19, 19.5, 20, 20.5, 21, 21.5])
if __name__ == '__main__':
    t1 = time.time()
    Mag_bin(19.5)
    t2 = time.time()
    print("bingo! yes!")
    print("The time equals to %s Minutes " % ((t2 - t1) / 60))





