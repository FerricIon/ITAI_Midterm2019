import json as js
import sys

def cf_recommend(input_movieID_list):
    cmsf=open('../data/cf_finalRcommend.json','r')
    cf_base=js.load(cmsf)
    cmsf.close()
    cf_recommendList={}
    for input_movieID in input_movieID_list:
        for options_movie in cf_base[str(input_movieID)]:
            if int(options_movie[0]) in input_movieID_list: #待推荐电影在输入电影列表中，跳过
                continue
            if options_movie[0] in cf_recommendList.keys(): #相似度数值累加
                cf_recommendList[options_movie[0]]+=options_movie[1]
            else:
                cf_recommendList[options_movie[0]]=options_movie[1]
    cf_result=sorted(cf_recommendList.items(),key=lambda it:it[1],reverse=True)
    cf_outputID=map(int, map(lambda o: o[0], cf_result[:10])) #结果取前十部电影
    return list(cf_outputID)

input_json = js.loads(input())
print(js.dumps(cf_recommend(input_json)))
