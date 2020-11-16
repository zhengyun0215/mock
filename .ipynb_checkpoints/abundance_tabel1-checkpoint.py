import numpy as np
import matplotlib.pyplot as plt
from AbundanceMatching import *
from scipy import integrate

boxsize = 600

subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_84.txt')

orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_84/orphantable_final.npy')

pos1 = np.concatenate((subhalo[:,7] / 1000 , orphan[:,6] / 1000))
pos2 = np.concatenate((subhalo[:,8] / 1000 , orphan[:,7] / 1000))
pos3 = np.concatenate((subhalo[:,9] / 1000 , orphan[:,8] / 1000))

v1 = np.concatenate((subhalo[:,10], orphan[:,9])
v2 = np.concatenate((subhalo[:,11], orphan[:,10])
v3 = np.concatenate((subhalo[:,12], orphan[:,11])
                    
vpeak = np.concatenate((subhalo[:,4], orphan[:,4]))
           
                    
stag=np.argsort(vpeak)
pos1=pos1[stag]
pos2=pos2[stag]
pos3=pos3[stag]

v1=v1[stag]
v2=v2[stag]
v3=v3[stag]

vpeak=vpeak[stag]
                    
                    
##SHAM
nd_halo= calc_number_densities(shm, boxsize)
arr=np.arange(10001)
hmbin = min(shm)+(max(shm)-min(shm))*arr/10000.
ndbin = calc_number_densities_in_bins(shm, boxsize, hmbin)

