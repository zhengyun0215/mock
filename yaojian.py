import numpy as np                                                                                                                     
from scipy.stats import truncnorm                                                                                                      

###########load magnitude###########                                                                                                   
newmag_99 = np.loadtxt('/home/yunzheng/mock/abundance_new/data/newmag_99.txt')                                                         
print(newmag_99.shape)                                                                                                                 
                                                                                                                                       
# ###########load Vpeak data###########                                                                                                
# subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_99.txt')                                                
                                                                                                                                       
# orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_99/orphantable_final.npy')                             
                                                                                                                                       
# vpeak = np.concatenate((subhalo[:,4], orphan[:,4]))                                                                                  
# stag = np.argsort(vpeak)                                                                                                             
# vpeak = vpeak[stag]                                                                                                                  
                                                                                                                                       
                                                                                                                                       
                                                                                                                                       
###########adding scatter############                                                                                                  
def mag_scatter(Mag):                                                                                                                 
    mu = Mag                                                                                                                          
    sigma = 0.8 + 0.4 * np.tanh(Mag + 20)                                                                                             
    lower, upper = mu - 2.5 * sigma, mu + 2.5 * sigma                                                                                 
    G = truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)                                                    
    return (G.rvs(1))                                                                                                                 
                                                                                                                                       
                                                                                                                                       
mags = []                                                                                                                             
for mag in newmag_99:                                                                                                                 
    x = mag_scatter(mag)                                                                                                              
    mags.append(x)                                                                                                                    
                                                                                                                                       
np.savetxt('/home/yunzheng/mock/abundance_new/data/scattermag/mag_99.txt',mags)  
