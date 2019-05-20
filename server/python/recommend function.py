import json as js
import nltk
import numpy

class movie:
    genre = []
    cast = []
    crew = []
    company = []
    spoken_languages = []
    keys = []
    keyword=[]
    root=set()
    ID = 0
    rate_average = 0
    rate_count = 0
    revenue = 0
    runtime = 0
    popularity = 0
    all_command_satisfied = False
    similarity_score = 0
    recommend_score = 0
    satisfied_score = 0

    def __init__(self,iD,GEN,CAST,CREW,COMPANY,KEY,LANGUAGE,RUNTIME,REVENUE,VOTE,VOTENUM,POP):
        self.ID=iD
        self.genre=GEN.copy()
        self.cast=CAST.copy()
        self.crew=CREW.copy()
        self.company=COMPANY.copy()
        self.keys=KEY.copy()
        self.spoken_languages=LANGUAGE.copy()
        self.runtime=RUNTIME
        self.revenue=REVENUE
        self.rate_average=VOTE
        self.rate_count=VOTENUM
        self.popularity=POP
        self.keyword=[]
        self.root=set()
        self.recommend_score = 0
        self.all_command_satisfied = False
        self.similarity_score = 0
        self.satisfied_score = 0

all_movies = []

with open('../data/recommendation.json','r',encoding='UTF-8') as file:
    filmdata = js.load(file)
with open('../data/keywords.json','r',encoding='UTF-8') as word_file:
    word_data=js.load(word_file)

for x in filmdata:
    all_movies.append(movie(x['id'],x['genre'],x['cast'],x['crew'],x['production_companies'],x['keywords'],x['spoken_languages'],x['runtime'],x['revenue'],x['rate_average'],x['rate_count'],x['popularity']))

keys_match={}
for x in word_data:
    keys_match[x[0]]=x[1]
    
    
for x in all_movies:
    for y in x.keys:
        x.keyword.append(keys_match[y])
    
test=all_movies[0].keyword
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
stemmer=PorterStemmer()

def extract_root(keyword_list):
    root=set()
    for x in keyword_list:
        words=x.split(' ')
        for y in words:
            y=y.lower()
            root.add(stemmer.stem(y))
    #去掉没有意义的虚词
    root.discard('and')
    root.discard('or')
    root.discard('the')
    root.discard('is')
    root.discard('of')
    root.discard('at')
    root.discard('a')
    root.discard('an')
    root.discard('on')
    root.discard('in')
    root.discard('will')
    root.discard('with')
    root.discard('to')
    root.discard('for')    
    return root

for x in all_movies:
    x.root=extract_root(x.keyword)

from nltk.corpus import wordnet
#对于输入的keyword列表生成它的同义词列表，扩大匹配范围，maxnum设定为对每个单词最多生成多少个同义词
def generate_syn(word_list,maxnum=10):
    syn_set=set()
    for x in word_list:
        words=x.split(' ')
        for y in words:
            cnt=0
            for syn in wordnet.synsets(y):
                for l in syn.lemmas():
                    if(cnt>maxnum):
                        break
                    syn_set.add(l.name())
                    cnt+=1
    return syn_set

#将处理过的用户输入的keyword与电影的keyword词根做比较，返回相同的数目
def keyword_compare(film,word_list):
    extended_words=generate_syn(word_list)
    processed_words=set()
    for x in extended_words:
        tmp=x.lower()
        tmp=tmp.replace('-','')
        tmp=tmp.replace('_',' ')
        processed_words.add(tmp)
    users_root=extract_root(processed_words)
    same_root=film.root.intersection(users_root)
    return len(same_root)

#将用户输入的其他数据（演职员等）与电影作比较，返回相同的数目
def genre_compare(film,data_list):
    same_set=set(film.genre).intersection(set(data_list))
    return len(same_set)

def cast_compare(film,cast_list):
    same_set1=set(film.cast).intersection(set(cast_list))
    return len(same_set1)

def crew_compare(film,crew_list):
    same_set1=set(film.crew).intersection(set(crew_list))
    return len(same_set1)

def company_compare(film,data_list):
    same_set=set(film.company).intersection(set(data_list))
    return len(same_set)

def language_compare(film,data_list):
    same_set=set(film.spoken_languages).intersection(set(data_list))
    return len(same_set)

#cf协同过滤:建立电影关联度矩阵cf_BasedOnMovie_sim.json，由属性相关度和用户同时喜爱数决定，后者暂无数据
'''def cfkeyword_compare(f1,f2):
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
            cf_temp=cfkeyword_compare(f1,f2)+genre_compare(f1,f2.genre)+cast_compare(f1,f2.cast)+crew_compare(f1,f2.crew)+company_compare(f1,f2.company)+language_compare(f1,f2.spoken_languages)
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
'''
def cf_recommend(input_movieID_list):
    cmsf=open('../data/cf_finalRcommend.json','r')
    cf_base=js.loads(cmsf)
    cmsf.close()
    cf_recommendList={}
    for input_movieID in input_movieID_list:
        for options_movie in cf_base[input_movieID]:
            if options_movie[0] in cf_recommendList.keys():
                cf_recommendList[options_movie[0]]+=options_movie[1]
            else:
                cf_recommendList[options_movie[0]]=options_movie[1]
    cf_result=sorted(cf_recommendList.items(),key=lambda it:it[1],reverse=True)
    cf_outputID=[]
    cf_outputID.append(x[0] for x in cf_result[0:9])
    return cf_outputID

#推荐函数在这里写
def recommendation(users_data):
    u_genre=users_data['genre'].copy()
    u_cast=users_data['cast'].copy()
    u_crew=users_data['crew'].copy()
    u_company=users_data['production_companies'].copy()
    u_keywords=users_data['keywords'].copy()
    u_spoken_languages=users_data['spoken_languages'].copy() 
    genre_command=(len(u_genre)>0)
    cast_command=(len(u_cast)>0)
    crew_command=(len(u_crew)>0)
    company_command=(len(u_company)>0)
    keywords_command=(len(u_keywords)>0)
    language_command=(len(u_spoken_languages)>0)
    for x in all_movies:
        genre_similarity=genre_compare(x,u_genre)
        cast_similarity=cast_compare(x,u_cast)
        crew_similarity=crew_compare(x,u_crew)
        company_similarity=company_compare(x,u_company)
        language_similarity=language_compare(x,u_spoken_languages)
        keyword_similarity=keyword_compare(x,u_keywords)
        #权重部分
        x.similarity_score=(2*genre_similarity+cast_similarity+crew_similarity+company_similarity+2*language_similarity+keyword_similarity)
        x.recommend_score=x.similarity_score*(((x.rate_average-5)*5) if x.rate_count>500 else ((x.rate_average-((500-x.rate_count/500)*2)-5)*5))+x.popularity/40

        x.satisfied_score=(genre_command and genre_similarity>0)+(cast_command and cast_similarity>0)+(crew_command and crew_similarity>0)+(company_command and company_similarity>0)+(language_command and language_similarity>0)+(keywords_command and keyword_similarity>0)     
        x.all_command_satisfied=((genre_command+cast_command+crew_command+company_command+language_command+keywords_command)==x.satisfied_score)
   
    from operator import attrgetter
    #所有输入要求都满足的最先排，然后是要求满足的越多越好，然后是推荐评分
    all_movies.sort(key=attrgetter('all_command_satisfied','satisfied_score','recommend_score'),reverse=True)
    recommend_list=[]
    for x in range(10):
        recommend_list.append(all_movies[x].ID)
    return recommend_list

input_json = js.loads(input())
print(recommendation(input_json))
