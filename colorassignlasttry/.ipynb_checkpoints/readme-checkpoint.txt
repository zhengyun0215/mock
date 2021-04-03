##########
1. colorassign.py
    分100000个红移bin做cdf插值
    用np.interp直接插值得到
    存文件：
    1）cdf_zform:/home/yunzheng/mock/color/data/zcdf_new/cdf_zform_3.npy
    2）color:/home/yunzheng/mock/color/data/zcdf_new/color_mul3.npy
    
    由assigncolor.pbs运行于fat节点
    
##########
2. colorassignnormal.py
    与colorassign.py程序内容一模一样
    但由于fat排队故放在normal跑
    存文件：
    1）cdf_zform:/home/yunzheng/mock/color/data/zcdf_new/cdf_zform_normal.npy
    2）color:/home/yunzheng/mock/color/data/zcdf_new/color_mul_normal.npy
    
    由assigncolor-Copy1.pbs运行于normal节点
    
############
3. colorassign_bins.py
    考虑到前两个程序要重复做插值，速度极慢，故用每个mag bin的中值代替各个星系的mag，直接分bin做插值
    在 jupyter：zform_new_3.ipynb中测试了直接用bin与单个插值得到的color差别不大
    但由于前两个程序跑出了结果所以没有实际运行
    后续若需要多个snapshot则可以考虑用这个脚本
    
