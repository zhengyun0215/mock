vmax_collection.py:

    vmax.pbs提交	
    
    x in range(100)
    np.savetxt('/home/yunzheng/mock/color/data/vmax/snapshot_%s.dat'%x)
    
    存所有subhalo从snapshot0 - 99的vmax值和出生snapshot

    vmax100_withlenth.out:程序的输出



len_subid.py:

    (这个程序是为vmax_select.py服务，但是后面vmax_select.py不被使用，所以这个程序也不再需要，但是可以快速知道每个snapshot的subhlao数目）
    
    len.pbs提交
    
    统计每个snapshot中subhalo的个数，即subid_len
    np.savetxt('/home/yunzheng/mock/color/data/len_all.txt',res)

    len_all.o7505:程序的输出



vmax_select.py:
    
    根据文章选择相应的vmax值，满足0.75*Vpeak
    这个程序跑不了啊！（由于multiprocessing的原因）
    
    zform.pbs提交
    
    
    
add_birthsnap.py:
    
    对subhalo的catalogue增加birthsnapshot
    
    birth_newcat.pbs提交
    
    np.save('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new.npy',a)
    存新的catalogue : snapshot_92_new.npy
    
    
    
zform_newcat.py:

    计算subhalo zform
    对包含birthsnapshot的新的catalogue:snapshot_92_new.npy 增加zform
    
    zform_newcat.pbs提交
    
    np.save('/home/yunzheng/mock/color/data/newcatalogue/snap_92_new_with_zform.npy',c)
    存新的catalogue : snapshot_92_new_with_zform.npy
    


zformcheck_copy.py:
    
    与zformcheck.py等价（我的代码有bug，选择copy运算）
    存单个Vpeak bin内的subhalo总数目和poor definition subhalo数目
    
    zformcheck.pbs提交
    
    np.save('/home/yunzheng/mock/color/data/newcatalogue/snap_92_new_new_zform.npy',c)
    存了两列数: N(total) 和 N(poor)




newcat_add_mag.py:

	对catalogue增加mag with scatter
	
	newcat_add_mag.pbs提交


	a = np.stack((subid,vpeak,pos_x,pos_y,pos_z,v_x,v_y,v_z,zform,newmag),axis= -1)	
	np.save('/home/yunzheng/mock/color/data/newcatalogue/snapshot_92_new_withmag.npy',a)
	存新的catalogue：snapshot_92_new_withmag.npy



