import numpy as np
import matplotlib.pyplot as plt
from AbundanceMatching import *
from scipy import integrate
import time
import multiprocessing as mp


boxsize = 600
print("Let's start! :)")

redshift = np.loadtxt('/home/yunzheng/mock/orphan/redshift.txt')

def mul(x):
    
    print("Multiprocessing start!")
    start = time.time()
    
    print("The snapshot id is %s"%x)
    
    subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_%s.txt'%x)

    orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_%s/orphantable_final.npy'%x)
    
    
#     pos1 = np.concatenate((subhalo[:,7] / 1000 , orphan[:,6] / 1000))
#     pos2 = np.concatenate((subhalo[:,8] / 1000 , orphan[:,7] / 1000))
#     pos3 = np.concatenate((subhalo[:,9] / 1000 , orphan[:,8] / 1000))

#     v1 = np.concatenate((subhalo[:,10], orphan[:,9])
#     v2 = np.concatenate((subhalo[:,11], orphan[:,10])
#     v3 = np.concatenate((subhalo[:,12], orphan[:,11])

    vpeak = np.concatenate((subhalo[:,4], orphan[:,4]))

                    
    stag=np.argsort(vpeak)
#     pos1=pos1[stag]
#     pos2=pos2[stag]
#     pos3=pos3[stag]

#     v1=v1[stag]
#     v2=v2[stag]
#     v3=v3[stag]

    vpeak=vpeak[stag]

                    
    ##SHAM
    
    ###luminosity function###
    #############################
    def luminosity_evolution(M,M_star0,phi_star0,alpha,P,Q,z):
        M_star = M_star0 - Q * (z - 0.1)
        phi_star = phi_star0 * np.power(10,0.4 * P * z)
        y = 0.4 * np.log(10) * phi_star * (np.power(10,(0.4 * (M_star - M)))) ** (1 + alpha) * np.exp(- 10 ** (0.4 * (M_star - M)))
        return y


    M_star_Blanton = -20.44
    phi_star_Blanton = 0.0149
    P_Blanton = 0.18
    Q_Blanton = 1.62
    alpha_Blanton = -1.05
    
    
    M_star_Loveday = -20.70
    phi_star_Loveday = 0.0094
    P_Loveday = 1.8
    Q_Loveday = 0.7
    alpha_Loveday = -1.23
    
    def omega(z):
        y = (1 + np.exp(-100 * (z - 0.15))) ** (-1)
        return y

    def phi_total(M,z):
        y = (1 - omega(z)) * luminosity_evolution(M,M_star_Blanton,phi_star_Blanton,alpha_Blanton,P_Blanton,Q_Blanton,z) + omega(z) * luminosity_evolution(M,M_star_Loveday,phi_star_Loveday,alpha_Loveday,P_Loveday,Q_Loveday,z)
        return y

    def luminosity_final(M,z):
        if z <= 0.1:
            phi_1 = luminosity_evolution(M,M_star_Blanton,phi_star_Blanton,alpha_Blanton,P_Blanton,Q_Blanton,z)
            return phi_1
        if 0.1 < z < 0.2:
            phi_2 = phi_total(M,z)
            return phi_2
        if z >= 0.2:
            phi_3 = luminosity_evolution(M,M_star_Loveday,phi_star_Loveday,alpha_Loveday,P_Loveday,Q_Loveday,z)
            return phi_3
    
    
    
    
    nstep=1001
    lfx0 = np.linspace(-25.,-10,nstep)
    lfy0 = luminosity_final(lfx0,redshift[x])
    print("Redshift is %s"%redshift[x])
    
    af = AbundanceFunction(lfx0,lfy0,(-25,-10))
    
    
    ######halo Vpeak density#####
    #############################
    nd_halo= calc_number_densities(vpeak, boxsize)
    
    
    ###########match###########
    newmag = af.match(nd_halo)
    
    
    np.savetxt('/home/yunzheng/mock/abundance_new/data/newmag_%d.txt'%x,newmag)

    
dat = np.array([84,85,86,87,88,89,91,92,94,95,97,99])


def multicore():
    pool = mp.Pool(processes = 36)
    res = pool.map(mul,dat)
    pool.close()
    pool.join()
    print("bingo! yes!")
    
    
if __name__ == '__main__':
    multicore()
    
