import h5py
import numpy as np
import time


print("Let's start! :)")

redshift = np.loadtxt('/home/yunzheng/mock/orphan/redshift.txt')

table = np.load('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new.npy')


###############读取vmax演化历史####################
vmax = []
for i in range(100):
    v = np.load('/home/yunzheng/mock/color/data/vmax/snapshot_%s.npy'%i)
    vmax.append(v)   
 

##########################存z_form####################
z_form = []

for i in range(len(table)):
    start = time.time()

    id_sub = int(table[i][0])
    vpeak = table[i][1]
    vform = vpeak * 0.75
    vsnap = int(table[i][2])
    vbirth = int(table[i][3])
               
    if i%5000 == 0:
        print('The subhalo id is %s'%(id_sub))
        print('The vpeak is %s'%(table[i][1]))
        print('The vform is %s'%(vform))
        print('i = %d'%i)
    
    if vsnap == vbirth:
#         print('The snapshot of vpeak equals to the birthsnap :%s'%vbirth)
        z_form.append(redshift[vsnap])
        print('The subhalo id is %s'%(id_sub))
               
    else:
#         print('The snapshot of vpeak is %s'%vsnap)
#         print('The snapshot of birth is %s'%vbirth)
        
        for k in range(vbirth,vsnap):
            if vmax[k][id_sub][1] <= vform < vmax[k+1][id_sub][1]:
                
#                 print('The snapshot of interpretation is between %s and %s .'%(k,k+1))
#                 print('The first redshift is %s'%(redshift[k]))
#                 print('The next redshift is %s'%(redshift[k+1]))
#                 print('The first vmax is %s'%(vmax[k][id_sub][1]))
#                 print('The next vmax is %s'%(vmax[k+1][id_sub][1]))
                
                interp_v = [vmax[k][id_sub][1],vmax[k+1][id_sub][1]]
                interp_z = [redshift[k],redshift[k+1]]
                red_new = np.interp(vform,interp_v,interp_z)
#                 print('The interplated redshift is %s'%red_new)
# #                 z_form.append(red_new)
#                 print('The snapshot number is %d'%k)
                break
                
            else:
#                 print("This subhalo couldn't interpolate")
                red_new = redshift[vbirth]
#                 z_form.append(redshift[vbirth])
#                 print('The snapshot number is %d'%k)
    
    
#         print('The snapshot number is %d'%k)
        z_form.append(red_new)
              


    
end = time.time()
print("time spent : %s minutes"%((end - start)/60))
    
               
               
c = np.column_stack((table,z_form))
               
               
np.save('/home/yunzheng/mock/color/data/newcatalogue/snap_92_new_with_zform.npy',c)

    
            
    
    
    
    
                        
                        
                        
                
                
        
    
