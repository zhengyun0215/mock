print('Start!')
import numpy as np
import multiprocessing as mp
import time


table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new_withmag.npy')
vpeak = table[:, 1]
zform = table[:, 8]
mag = table[:, 9]

print(np.max(zform))
print(np.min(zform))

##########  分100000个红移bin  ############
arr_red = np.arange(100001)
bin_red = 0.21 + 12.2 * arr_red / 100000

##########  分80个mag bin ##############
mag_bin_new = np.array([-23.5, -23.0, -22.8, -22.7,
                        -22.6, -22.5, -22.4, -22.3, -22.2, -22.1, -22., -21.9, -21.8,
                        -21.7, -21.6, -21.5, -21.4, -21.3, -21.2, -21.1, -21., -20.9,
                        -20.8, -20.7, -20.6, -20.5, -20.4, -20.3, -20.2, -20.1, -20.,
                        -19.9, -19.8, -19.7, -19.6, -19.5, -19.4, -19.3, -19.2, -19.1,
                        -19., -18.9, -18.8, -18.7, -18.6, -18.5, -18.4, -18.3, -18.2,
                        -18.1, -18., -17.9, -17.8, -17.7, -17.6, -17.5, -17.4, -17.3,
                        -17.2, -17.1, -17., -16.9, -16.8, -16.7, -16.6, -16.5, -16.4,
                        -16.3, -16.2, -16.1, -16., -15.9, -15.8, -15.7, -15.6, -15.5,
                        -15.4, -15.3, -15.2, -15.1])
print(mag_bin_new.shape)

###########  分不同的mag bin存储vpeak 、 zform  ###########
inds = np.digitize(mag, mag_bin_new)

############ 尝试把subhalo信息都存成一行方便查找  ##########
total_bin = [[] for _ in range(80)]
for n in range(len(vpeak)):
    sub_info = np.array((vpeak[n], zform[n], mag[n]))
    total_bin[inds[n]].append(sub_info)

for i in range(80):
    print(len(total_bin[i]))

############ 统计每个mag bin内的zform cdf  ############
total_cdf = [[] for _ in range(80)]
for i in range(1, 80):
    info = np.array(total_bin[i])
    hist_temp = np.histogram(info[:, 1], bin_red)[0]
    cdfbin = np.cumsum(hist_temp) / sum(hist_temp)
    total_cdf[i].append(cdfbin)

##########  做插值得到每个subhalo zform对应的cdf  ###########
cdf_zform = np.zeros(len(vpeak))
for n in range(len(vpeak)):
    cdf_zform[n] = np.interp(zform[n], bin_red[1:], total_cdf[inds[n]][0])
print(cdf_zform.shape)
np.save('/home/yunzheng/mock/color/data/zcdf_new/cdf_zform_3.npy', cdf_zform)
print("The maximum of cdf_zform is:",np.max(cdf_zform))
print("The minimum of cdf_zform is:",np.min(cdf_zform))

########  经验公式求color  ##########
########  定义fraction of blue galaxies  #############
from scipy.stats import norm


def blue(M):
    if M < -26.571428571428571:
        y = 0
        return y
    elif (M < -19.53846153846154):
        y = 0.46 + 0.07 * (M + 20)
        return y
    elif M < -17.1733389977005:
        y = 0.4 + 0.2 * (M + 20)
        return y
    else:
        y = 1 / (1 + np.exp(- (M + 20.5)))
        return y

def mu_blue(M,z):
    y = 0.62 - 0.11 * (M + 20) - 0.25 * (min(z,0.4) - 0.1)
    return y
def sigma_blue(M,z):
    y = 0.12 + 0.02 * (M + 20) + 0.2 * (z - 0.1)
    return y
def mu_red(M,z):
    y = 0.932 - 0.032 * (M + 20) - 0.18 * (min(z,0.4) - 0.1)
    return y
def sigma_red(M,z):
    y = 0.07 + 0.01 * (M + 20) + 0.5 * (z - 0.1) + 0.1 * (z - 0.1)**2
    return y


def cdf(col, M, z):
    y = blue(M) * norm.cdf(col, loc=mu_blue(M, z), scale=sigma_blue(M, z)) + (1 - blue(M)) * norm.cdf(col, loc=mu_red(M, z), scale=sigma_red(M,z))
    return y


def pdf(col, M, z):
    y = blue(M) * norm.pdf(col, loc=mu_blue(M, z), scale=sigma_blue(M, z)) + (1 - blue(M)) * norm.pdf(col,loc=mu_red(M, z), scale=sigma_red(M,z))
    return y


z0 = 0.2182580231028184


st1 = time.time()

color0 = np.linspace(-1.5,2.2,10000000)
def colorassign(mag,cdf_z):
    distest = cdf(color0,mag,z0)
    finalcolor = np.interp(cdf_z,distest,color0)
    return finalcolor

def mul(count):
    if count % 100000 == 0:
        print('count=', count)
    mul_col = colorassign(mag[count],cdf_zform[count])
    return (mul_col)


pro = mp.Pool(processes=80)
res = pro.map(mul, range(26241654))
np.save('/home/yunzheng/mock/color/data/zcdf_new/color_mul3.npy', res)
pro.close()
pro.join()
st2 = time.time()
print("time spent : %s minutes" % ((st2 - st1) / 60))
print("bingo! yes!")




