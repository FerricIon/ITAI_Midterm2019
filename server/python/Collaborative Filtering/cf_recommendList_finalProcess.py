import json as js
#将协同过滤所得相似矩阵整合进简单过滤所得的前四十推荐列表的相似度数值中，重新排一次序，{movieID: [[movieID, sim], ...], ...}导出至cf_recommend_BasedOnMovie.json
mfile=open('cf_recommend_BasedOnMovie.json','r')
pre_recommend=js.load(mfile)
mfile.close()
mfile=open('cf_matrix_BasedonUser.json','r')
userBased_mat=js.load(mfile)
mfile.close()
data={}
for mid1 in pre_recommend.keys():
    data[mid1]=[]
    for ms in pre_recommend[mid1]:
        if mid1 in userBased_mat.keys() and str(ms[0]) in userBased_mat.keys():
            data[mid1].append([str(ms[0]),ms[1]+8*userBased_mat[mid1][str(ms[0])]])
        else:
            data[mid1].append([str(ms[0]),ms[1]])
    data[mid1].sort(key=lambda it: it[1],reverse=True)
mfile=open('cf_finalRcommend.json','w')
mfile.write(js.dumps(data))
mfile.close()