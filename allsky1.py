# -*- coding:utf-8 -*-
import numpy as np
# from nbodykit import transform
import scipy
import dask.array as da
from astropy.constants import c
from scipy.interpolate import interp1d
import astropy.units as u
from astropy.cosmology import FlatLambdaCDM, z_at_value
import pathos.multiprocessing as pmp


x = np.empty(0)
y = np.empty(0)
z = np.empty(0)
for i in range(7):
    for j in range(7):
        for q in range(7):
            x = np.append(x,i)
            y = np.append(y,j)
            z = np.append(z,q)
            print(i,j,q)

##############load table###############
table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_final.npy.npz')
print(table.files)
############definition of cosmology ###########
cosmo = FlatLambdaCDM(H0=100, Om0=0.268, Tcmb0=2.725)
h = cosmo.h
print("The value of h equals to:", h)
###########reading catalogue############
subid = table['subid']
mass = table['mass']
posx = table['posx'] / 1000
posy = table['posy'] / 1000
posz = table['posz'] / 1000  #########转化为Mpc/h

vx = table['vx']
vy = table['vy']
vz = table['vz']

mag = table['mag']
color = table['color']
print("The length of mag is", mag.shape)

#############setting the initial properties###############
lbox = 600
cellx = posx
celly = posy
cellz = posz
subid01 = subid
mass01 = mass
mag01 = mag
color01 = color

##############define function for stacking box##############
def stack_box(a,b,c):
    xx = np.empty(0)
    xy = np.empty(0)
    xz = np.empty(0)
    vx_new = np.empty(0)
    vy_new = np.empty(0)
    vz_new = np.empty(0)
    subid_new = np.empty(0)
    mass_new = np.empty(0)
    mag_new = np.empty(0)
    color_new = np.empty(0)

    topx = cellx + a * lbox
    topy = celly + b * lbox
    topz = cellz + c * lbox
    
    xx = np.append(xx,topx)
    xy = np.append(xy,topy)
    xz = np.append(xz,topz)

    vx_new = np.append(vx_new, vx)
    vy_new = np.append(vy_new, vy)
    vz_new = np.append(vz_new, vz)
    subid_new = np.append(subid_new, subid01)
    mass_new = np.append(mass_new, mass01)
    mag_new = np.append(mag_new, mag01)
    color_new = np.append(color_new, color01)

    newox = xx - 2100.0 - 51.4
    newoy = xy - 2100.0 - 102.3
    newoz = xz - 2100.0 - 131.2

    pos_new = np.stack((newox, newoy, newoz), axis=-1)
    vel_new = np.stack((vx_new, vy_new, vz_new), axis=-1)

    print("The length of total boxes is: ", newox.shape)
    print("This is the box : x = %s,y = %s,z = %s"%(a,b,c))
    print("The min/max x :", (np.min(newox), np.max(newox)))
    print("The min/max y :", (np.min(newoy), np.max(newoy)))
    print("The min/max z :", (np.min(newoz), np.max(newoz)))


    ##############坐标系转换################
    ##############计算ra dec###############
    s = np.hypot(newox, newoy)
    ra0 = np.arctan2(newoy, newox)
    dec0 = np.arctan2(newoz, s)
    lon = np.rad2deg(ra0)
    lat = np.rad2deg(dec0)
    lon = np.mod(lon - 360.0, 360.0)
    ra, dec = lon, lat
    print("The minimum value of ra:", np.min(ra0))
    print("The maximum value of ra:", np.max(ra0))

    ##############计算共动距离################
    dcom0 = da.linalg.norm(pos_new,axis=-1)
    print("The minimum value of comoving distance:", np.min(dcom0))
    print("The maximum value of comoving distance:", np.max(dcom0))

    ##############利用插值的方法得到共动距离对应的红移################
    redshift = np.linspace(0.0, 1.0, 10000000)
    cd = cosmo.comoving_distance(redshift) * h  ###############Mpc/h
    print("The length of the cd:", len(cd))
    cd = cd.value
    zreal = np.interp(dcom0,cd,redshift)

    ############计算红移畸变###############
    vpec = (pos_new * vel_new).sum(axis=-1)/dcom0
    cv = c.to('km/s').value
    print("The light speed is:", cv)
    zobs = zreal + vpec * (1 + zreal) /cv

    print("The all boxes range:")
    print("The length of catalogue is:", ra.shape)
    print("RA range:", (np.min(ra), np.max(ra)))
    print("dec range:", (np.min(dec), np.max(dec)))
    print("The redshift of real distance range:",(np.min(zreal),np.max(zreal)))
    print("The redshift of observation range:", (np.min(zobs), np.max(zobs)))

    ############视星等转化为绝对星等#############
    d_lum = (1 + zreal) * dcom0
    dismod = 25.0 + 5 * np.log10(d_lum)
    appmag = mag_new + dismod
    print("The apparent magnitudes have been finished!")
    print("The apparent magnitudes range is: ", (np.min(appmag), np.max(appmag)))

    ###########flux cut##############
    flscut = (appmag <= 20.0 )
    subid_new = subid_new[flscut]
    ra = ra[flscut]
    dec = dec[flscut]
    dcom = dcom0[flscut]
    zreal = zreal[flscut]
    zobs = zobs[flscut]
    appmag = appmag[flscut]
    color_new = color_new[flscut]
    mag_new = mag_new[flscut]

    ##############
    np.savez("/home/yunzheng/mock/box_replication/data/boxes/box_%d_%d_%d.npz"%(a,b,c), subid=subid_new, ra=ra, dec=dec,dcom = dcom,zreal = zreal, zobs=zobs, appmag=appmag, absmag=mag_new, color=color_new)

    
def multicore():
    pool = pmp.ProcessingPool(processes = 1)
    res = pool.map(stack_box, x, y, z)
    pool.close()
    pool.join()
    print("Bingo!Yes!")
    
if __name__ == '__main__':
    multicore()



    
