vmax_collection.py:
    vmax.pbs提交	
    x in range(100)
    np.savetxt('/home/yunzheng/mock/color/data/vmax/snapshot_%s.dat'%x)
    
    存所有subhalo从snapshot0 - 99的vmax值和出生snapshot

    vmax100_withlenth.out:程序的输出



len_subid.py:
    len.pbs提交
    统计每个snapshot中subhalo的个数，即subid_len
    np.savetxt('/home/yunzheng/mock/color/data/len_all.txt',res)

    len_all.o7505:程序的输出



vmax_select.py:
    
    根据文章选择相应的vmax值，满足0.75*Vpeak
