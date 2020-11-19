import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import plot,savefig


print("Let's start! :)")


subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_%s.txt'%x)

orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_%s/orphantable_final.npy'%x)





x=np.linspace(-4,4,30)
y=np.sin(x);
plot(x,y,'--*b')
savefig('D:/MyFig.jpg')



print(help(AbundanceFunction))
boxsize = 600

