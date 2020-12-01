1.findorphan_1.py
并行从snapshots:[84,85,86,87,88,89,91,92,94,95,97,99] 中初步筛选出满足orphan的subhalo：
筛选条件：
	粒子数为1；rank & depth > 0 ; sinkid < 0 ; 最大粒子数 大于50
存文件：
在每个subhalo 最后一次作为central subhalo的snapshot存其信息：
	for i in range(100):
	        np.save('/home/yunzheng/mock/orphan_new/orphantabel_new/snapshot_%d/orphantable_savetest_%d.npy'%(x,i),orphantable[i])


统计每个snapshot中有多少个orphan 候选者：
	np.savetxt('/home/yunzheng/mock/orphan_new/orphantabel_new/snapshot_%d/fsnapnum.txt'%x,fsnapnum)    
    	
依次为：
	subhaloid
	masspeak
	snapshot of masspeak
	Last isolation snapshot
	Vmaxpeak
	Snapshot of Vmaxpeak
	Position x, y , z
	Velocity x, y , z
共12个data


orphanfirstselection = firstfindorphan.out
记录了每个snapshot的初次筛选orphan的结果和时间

2.multest.py
