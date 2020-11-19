import numpy as np
import numpy as np
from scipy import integrate
from AbundanceMatching import *

print(help(AbundanceFunction))
boxsize = 600
print("Let's start! :)")

redshift = np.loadtxt('/home/yunzheng/mock/orphan/redshift.txt')

def gogo():
    print(redshift.shape)

if __name__ == '__main__':
    gogo()
