
print('Strat!')

import numpy as np
from Corrfunc.theory.wp import wp
import time
# from Corrfunc.theory import DDrppi
# from Corrfunc.utils import convert_rp_pi_counts_to_wp

table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new_withcolor.npz')
print(table.files)

posx = table['posx'] / 1000
posy = table['posy'] / 1000
posz = table['posz'] / 1000

color = table['color']
mag = table['mag']

print('Load Sucessfully!')


##########  box参数  ##########
boxsize0 = 600
pimax0 = 60
nthreads0 = 30
aa = np.linspace(-2., 1.8, 20)
bins0 = 10. ** aa
nrpbins0 = len(bins0) - 1
print('Box parameters Sucessfully!')



def Mag_bin(i):
    t1 = time.time()
    print('The Mag bin is %s'%i)
    
    temp = (mag < i) & (mag > i-1)
    mag_bin = mag[temp]
    print("The maximum mag is",(np.max(mag_bin)))
    print("The minimum mag is",(np.min(mag_bin)))
    print("The length of this mag bin is ",len(mag_bin))
    x_bin = posx[temp]
    y_bin = posy[temp]
    z_bin = posz[temp]
    
    color_bin = color[temp]
    print("The length of color is:",len(color_bin))
    color_cut = 0.21 - 0.03 * mag_bin
    redtemp = color_bin > color_cut
    bluetemp = (1-redtemp).astype(bool)
    
    redcolor = color_bin[redtemp]
    print("The maximum color of red galaxies is :",np.max(redcolor))
    print("The minimum color of red galaxies is :",np.min(redcolor))
    bluecolor = color_bin[bluetemp]
    print("The maximum color of blue galaxies is :",np.max(bluecolor))
    print("The minimum color of blue galaxies is :",np.min(bluecolor))
    
    #############  assign color positions #################
    redx = x_bin[redtemp]
    redy = y_bin[redtemp]
    redz = z_bin[redtemp]
    print("The length of redx is :",len(redx))
    print("The first position of red galaxy is :",redx[0])
    bluex = x_bin[bluetemp]
    bluey = y_bin[bluetemp]
    bluez = z_bin[bluetemp]
    print("The length of bluex is :",len(bluex))
    print("The first position of blue galaxy is :",bluex[0])
    
    ##############  calculate the projection CF ##############
    results = wp(boxsize0,pimax0,nthreads0,bins0,x_bin,y_bin, z_bin,output_rpavg=True)
    redresults = wp(boxsize0,pimax0,nthreads0,bins0,redx,redy, redz,output_rpavg=True)
    blueresults = wp(boxsize0,pimax0,nthreads0,bins0,bluex,bluey, bluez,output_rpavg=True)
#     Corrfunc.theory.wp(boxsize, pimax, nthreads, binfile, X, Y, Z, weights=None, weight_type=None, verbose=False, output_rpavg=False, xbin_refine_factor=2, ybin_refine_factor=2, zbin_refine_factor=1, max_cells_per_dim=100, copy_particles=True, enable_min_sep_opt=True, c_api_timer=False, c_cell_timer=False, isa=u'fastest')
    
    
    np.savez('/home/yunzheng/mock/clustering/data/wp_color/wp3_total_%s.npz'%i,rp = results['rpavg'],wp = results['wp'])
    np.savez('/home/yunzheng/mock/clustering/data/wp_color/wp3_red_%s.npz' % i, rp = redresults['rpavg'],wp = redresults['wp'])
    np.savez('/home/yunzheng/mock/clustering/data/wp_color/wp3_blue_%s.npz' % i, rp = blueresults['rpavg'],wp = blueresults['wp'])
    t2 = time.time()
    
    print("The time for this mag bin is %s minutes "%((t2-t1)/60))

    
dat = np.array([19,20,21])
dat = -dat
print(dat)


if __name__ == '__main__':
    for i in (dat):
        Mag_bin(i)
    




