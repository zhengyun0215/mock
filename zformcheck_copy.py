
import numpy as np



print("Let's start! :)")

redshift = np.loadtxt('/home/yunzheng/mock/orphan/redshift.txt')

table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snap_92_new_with_zform.npy')

###############读取vmax演化历史####################
vmax = []
for i in range(100):
    v = np.load('/home/yunzheng/mock/color/data/vmax/snapshot_%s.npy'%i)
    vmax.append(v)   
 


vpeak = table[:,1]
birth = table[:,3]
birth_in = np.array(birth,dtype = 'int')


bin_0 = np.arange(30,1841,5)
inds = np.digitize(vpeak,bin_0)


num_total = np.zeros(363)
num_poor = np.zeros(363)

for i in range(len(vpeak)):
    
    num_total[inds[i]] = num_total[inds[i]] + 1

    id_sub = int(table[i][0])
    vpeak_0 = vpeak[i]
    vform = vpeak_0 * 0.75
    vsnap = int(table[i][2])
    vbirth = int(birth_in[i])
               
    if i%5000 == 0:
        print('The subhalo id is %s'%(id_sub))
        print('The vpeak is %s'%(table[i][1]))
        print('The vform is %s'%(vform))
        print('i = %d'%i)
    
    if vsnap == vbirth:
#         print('The snapshot of vpeak equals to the birthsnap :%s'%vbirth)
        num_poor[inds[i]] = num_poor[inds[i]] + 1
        print('The subhalo id is %s'%(id_sub))
               
    else:
#         print('The snapshot of vpeak is %s'%vsnap)
#         print('The snapshot of birth is %s'%vbirth)
        
        for k in range(vbirth,vsnap):
            if vmax[k][id_sub][1] <= vform < vmax[k+1][id_sub][1]:
                num_test = 0
                break
                
            else:
#                 print("This subhalo couldn't interpolate")
                num_test = 1
    
        num_poor[inds[i]] = num_poor[inds[i]] + num_test


c = np.column_stack((num_poor,num_total))
               
np.save('/home/yunzheng/mock/color/data/newcatalogue/snap_92_new_new_zform.npy',c)

    
            
    
    
    
    
                        
                        
                        
                
                
        
    

