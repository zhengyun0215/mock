import multiprocessing as mp
import time
import numpy as np

def job_1(x):
    
    y = x**2
    if x%10000000 ==0:
        print("subhalo id is %d"%x)
        
        np.savetxt('/home/yunzheng/mock/orphan_new/code/savetest/test_%s.txt'%x,[y])



def multicore():
    pool = mp.Pool(processes = 64)
    res = pool.map(job_1,range(100000000))
#     np.savetxt('/home/yunzheng/mock/orphan_new/test_%d.txt'%i,res)
#     print(res)
    
    
    
if __name__ == '__main__':
    st1 = time.time()
    multicore()
    st2 = time.time()
    print('time:',(st2 - st1))