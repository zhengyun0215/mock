import h5py
import numpy as np
import time
# import multiprocessing as mp


print("Let's start! :)")

redshift = np.loadtxt('/home/yunzheng/mock/orphan/redshift.txt')

subhalo = np.loadtxt('/home/yunzheng/mock/subhalos_new/subhalotable/snapshot_92.txt')

orphan = np.load('/home/yunzheng/mock/orphan_new/final_selection_new/snapshot_92/orphantable_final.npy')

#################存subhalo和orphan的id和速度############


subid = np.concatenate((subhalo[:,0], orphan[:,0]))
subid = np.array(subid,dtype = int)
a = len(subid)
print('The length is %d'%a)

vpeak = np.concatenate((subhalo[:,4], orphan[:,4]))

vpeaksnap = np.concatenate((subhalo[:,5], orphan[:,5]))
vpeaksnap = np.array(vpeaksnap,dtype = 'int')

orp_mass = np.ones(len(orphan)) * 0.05541996
mass = np.concatenate((subhalo[:,6],orp_mass))

pos_x = np.concatenate((subhalo[:,7], orphan[:,6]))
pos_y = np.concatenate((subhalo[:,8], orphan[:,7]))
pos_z = np.concatenate((subhalo[:,9], orphan[:,8]))

v_x = np.concatenate((subhalo[:,10], orphan[:,9]))
v_y = np.concatenate((subhalo[:,11], orphan[:,10]))  
v_z = np.concatenate((subhalo[:,12], orphan[:,11]))                           

print(subid.shape)
print(vpeak.shape)
print(mass.shape)


################导入所有vmax文件####################

len_all = np.loadtxt('/home/yunzheng/mock/color/data/len_all.txt')

###############读取vmax演化历史####################
vmax = []
for i in range(100):
    v = np.load('/home/yunzheng/mock/color/data/vmax/snapshot_%s.npy'%i)
    vmax.append(v)   
    
    
subhalotable_new = []

for i in range(a):

    print("Circle start!")
    start = time.time()


    ################重新存subhalotable####################

    vform =  vpeak[i] * 0.75
    
    if i%5000 == 0:
        
        print('i = %d'%i)
        print('The subhalo id is %s'%(subid[i]))
    
    for j in range(100):
        
        if subid[i] <= len_all[j] -1:
#             print('The birthsnap of %dth subhalo is %d'%(subid[i],j))
#             print('The birthsnap check is %d'%(vmax[j][subid[i]][2]))
#             # print('j = %d'%j)

            for k in range(j,vpeaksnap[i]):

                if vmax[k][subid[i]][1] <= vform < vmax[k+1][subid[i]][1]:
       
                    print('The snapshot of interpretation is between %s and %s .'%(k,k+1))
                    print('The first redshift is %s'%(redshift[k]))
                    print('The next redshift is %s'%(redshift[k+1]))
                    print('The first vmax is %s'%(vmax[k][subid[i]][1]))
                    print('The next vmax is %s'%(vmax[k+1][subid[i]][1]))
                    interp_v = [vmax[k][subid[i]][1],vmax[k+1][subid[i]][1]]
                    interp_z = [redshift[k],redshift[k+1]]
                    red_new = np.interp(vform,interp_v,interp_z)
                    print('The interplated redshift is %s'%red_new)
                    form_all = np.array((subid[i],vpeak[i],vpeaksnap[i],j,vform,red_new,mass[i],pos_x[i],pos_y[i],pos_z[i],v_x[i],v_y[i],v_z[i]))
                    subhalotable_new.append(form_all)
                    break

                else:
                    snap_bir = j
                    print('The snapshot of birth is %s'%snap_bir)
                    print('The vmax is %s'%vmax[k][subid[i]][1])
                    red_new = redshift[j]
                    print('The redshift is %s'%red_new)
                    form_all = np.array((subid[i],vpeak[i],vpeaksnap[i],j,vform,red_new,mass[i],pos_x[i],pos_y[i],pos_z[i],v_x[i],v_y[i],v_z[i]))
                    subhalotable_new.append(form_all)
                    break
                    
#                 print('The circle number is %s'%k)
#             print('j = %d'%j)

            
            break
    # print(z_form)

    
    
    end = time.time()
    print("time spent : %s minutes"%((end - start)/60))
    
np.save('/home/yunzheng/mock/color/data/newcatalogue/snap_92_1.npy',subhalotable_new)

    
            
    
    
    
    
                        
                        
                        
                
                
        
    