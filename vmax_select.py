import h5py
import numpy as np
import time
import multiprocessing as mp


print("Let's start! :)")

redshift = np.loadtxt('/home/yunzheng/mock/orphan/redshift.txt')


def selec(x):
    
    print("Multiprocessing start!")
    start = time.time()
    
    print("The snapshot id is %s"%x)
    
    subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_%s.txt'%x)

    orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_%s/orphantable_final.npy'%x)