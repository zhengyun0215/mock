#############
allsky1:
用pathos.multiprocessing去叠盒子
报错：OSError: [Errno 12] Cannot allocate memory

#############
allsky2:
用multiprocessing.pool.starmap叠盒子(多参数xyz)
仅用5个cpu跑并行


输出: np.savez("/home/yunzheng/mock/box_replication/data/boxes/box_%d_%d_%d.npz"%(a,b,c), subid=subid_new, ra=ra, dec=dec,dcom = dcom,zreal = zreal, zobs=zobs, appmag=appmag, absmag=mag_new, color=color_new)



##########
allsky3:
    step 1:
        红移cut : z~0.5 
    step 2:
        视星等cut: app_mag < 20.6
        
输出:
 np.savez("/home/yunzheng/mock/box_replication/data/boxes2/box_%d_%d_%d.npz" % (a, b, c), subid=subid_new, ra=ra,
                 dec=dec, dcom=dcom, zreal=zreal, zobs=zobs, appmag=appmag, absmag=mag_new, color=color_new,
                 halo_mass=mass_new, pos=pos_new, vel=vel_new)
    
    
