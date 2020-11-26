import numpy as np
from scipy.stats import truncnorm
import multiprocessing as mp

print("Start! :)")

###########load magnitude###########
newmag_92 = np.loadtxt('/home/yunzheng/mock/abundance_new/data/newmag_92.txt')
print(newmag_92.shape)


###########load Vpeak data###########
subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_92.txt')

orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_92/orphantable_final.npy')

vpeak = np.concatenate((subhalo[:,4], orphan[:,4]))
stag = np.argsort(vpeak)
vpeak = vpeak[stag]

np.savetxt('/home/yunzheng/mock/abundance_new/data/largedata/vpeak_92.txt',vpeak)
print(vpeak.shape)


###########adding scatter############
def mag_scatter(Mag):
    mu = Mag
    sigma = 0.8 + 0.4 * np.tanh(Mag + 20)
    lower, upper = mu - 2.5 * sigma, mu + 2.5 * sigma 
    G = truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma) 
    return (G.rvs(1))



def multicore():
    pool = mp.Pool(processes = 64)
    res = pool.map(mag_scatter,newmag_92)
    np.savetxt('/home/yunzheng/mock/abundance_new/data/scattermag/mag_92.txt',res)
    pool.close()
    pool.join()
    print("bingo! yes!")
    

if __name__ == '__main__':
    multicore()
