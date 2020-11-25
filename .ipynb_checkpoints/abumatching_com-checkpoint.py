import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from AbundanceMatching import *


print("Let's start! :)")


subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_99.txt')

orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_99/orphantable_final.npy')

vpeak = np.concatenate((subhalo[:,4], orphan[:,4]))
stag = np.argsort(vpeak)
vpeak = vpeak[stag]
nd_halos = calc_number_densities(vpeak,600)



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


lfBlanton = np.loadtxt('/home/yunzheng/code/yanglei/yanglei/data/full1/vmax/lfvmax-q2.00a-1.00.dr72full1.dat')
lfB03x=lfBlanton[:,0]
lfB03y=lfBlanton[:,1]

af = AbundanceFunction(lfB03x, lfB03y, (-27, -5))
catalog = af.match(nd_halos)

nstep=1000
lfx0 = np.linspace(-25,-15,nstep)
lfy_test = luminosity_final(lfx0,0.1)
af_test = AbundanceFunction(lfx0,lfy_test,(-25,-10))
catalog_test = af_test.match(nd_halos)



plt.scatter(vpeak,catalog,s = 0.05)
plt.scatter(vpeak,catalog_test,s=0.05,marker = '*')

plt.title(r'Matched set comparison')
plt.xlabel(r' $Vpeak$ ')
plt.ylabel(r'Magnitude')
plt.legend(('dr7','evoLF'))

plt.savefig('/home/yunzheng/mock/abundance_new/picture/Matchfail.pdf',dpi = 100)

