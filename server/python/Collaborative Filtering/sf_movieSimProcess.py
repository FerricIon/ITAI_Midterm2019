#利用简单过滤的成果，对5000电影选取相同属性/标签个数最多的前40部电影并降序排列（减小内存，提高效率），{movieID: [[movieID, sim], ...], ...}导出至cf_BasedOnMovie_sim.json
def cfkeyword_compare(f1,f2):
    same_set=f1.root.intersection(f2.root)
    return len(same_set)
cf_temp=0
cf_BasedOnMovie_sim={}
cmsf=open('../data/cf_BasedOnMovie_sim.json','w')
for f1 in all_movies:
    for f2 in all_movies:
        if f1.ID < f2.ID:
            if f1.ID not in cf_BasedOnMovie_sim.keys():
                cf_BasedOnMovie_sim[f1.ID]=[]
            if f2.ID not in cf_BasedOnMovie_sim.keys():
                cf_BasedOnMovie_sim[f2.ID]=[]
            #相同属性/标签个数cf_temp：
            cf_temp=cfkeyword_compare(f1,f2)+genre_compare(f1,f2.genre)+cast_compare(f1,f2.cast)+crew_compare(f1,f2.crew)+company_compare(f1,f2.company)+language_compare(f1,f2.spoken_languages)
            #限定只保留相似度最高前40部：
            if len(cf_BasedOnMovie_sim[f1.ID])<40:
                cf_BasedOnMovie_sim[f1.ID].append([f2.ID,cf_temp])
                if len(cf_BasedOnMovie_sim[f1.ID])==40:
                    cf_BasedOnMovie_sim[f1.ID].sort(key=lambda it: it[1],reverse=True)
            if len(cf_BasedOnMovie_sim[f2.ID])<40:
                cf_BasedOnMovie_sim[f2.ID].append([f1.ID,cf_temp])
                if len(cf_BasedOnMovie_sim[f2.ID])==40:
                    cf_BasedOnMovie_sim[f2.ID].sort(key=lambda it: it[1],reverse=True)
            if len(cf_BasedOnMovie_sim[f1.ID])>=40 and cf_temp>cf_BasedOnMovie_sim[f1.ID][39][1]:
                cf_BasedOnMovie_sim[f1.ID][39] = [f2.ID,cf_temp]
                cf_BasedOnMovie_sim[f1.ID].sort(key=lambda it: it[1],reverse=True)
            if len(cf_BasedOnMovie_sim[f2.ID])>=40 and cf_temp>cf_BasedOnMovie_sim[f2.ID][39][1]:
                cf_BasedOnMovie_sim[f2.ID][39] = [f1.ID,cf_temp]
                cf_BasedOnMovie_sim[f2.ID].sort(key=lambda it: it[1],reverse=True)
cffile_w=js.dumps(cf_BasedOnMovie_sim)
cmsf.write(cffile_w)
cmsf.close()