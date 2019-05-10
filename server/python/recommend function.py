import json as js
import nltk
import numpy
class movie:
    genre = []
    cast = []
    crew = []
    company = []
    spoken_lauguages = []
    keys = []
    keyword=[]
    root=set()
    ID = 0
    rate_average = 0
    rate_count = 0
    revenue = 0
    runtime = 0
    popularity = 0
    recommend_score = 0

    def __init__(self,iD,GEN,CAST,CREW,COMPANY,KEY,LANGUAGE,RUNTIME,REVENUE,VOTE,VOTENUM,POP):
        self.ID=iD
        self.genre=GEN.copy()
        self.cast=CAST.copy()
        self.crew=CREW.copy()
        self.company=COMPANY.copy()
        self.keys=KEY.copy()
        self.spoken_lauguages=LANGUAGE.copy()
        self.runtime=RUNTIME
        self.revenue=REVENUE
        self.rate_average=VOTE
        self.rate_count=VOTENUM
        self.popularity=POP
        self.keyword=[]
        self.root=set()
        self.recommend_score = 0

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
print(stemmer.stem(''))

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

def staff_compare(film,cast_list,crew_list):
    same_set1=set(film.cast).intersection(set(cast_list))
    same_set2=set(film.crew).intersection(set(crew_list))
    return (len(same_set1)+len(same_set2))

def company_compare(film,data_list):
    same_set=set(film.company).intersection(set(data_list))
    return len(same_set)

def language_compare(film,data_list):
    same_set=set(film.spoken_lauguages).intersection(set(data_list))
    return len(same_set)

#推荐函数在这里写
def recommendation(users_data):
    u_genre=users_data['genre'].copy()
    u_cast=users_data['cast'].copy()
    u_crew=users_data['crew'].copy()
    u_company=users_data['production_companies'].copy()
    u_keywords=users_data['keywords'].copy()
    u_spoken_languages=users_data['spoken_languages'].copy()
    for x in all_movies:
        genre_similarity=genre_compare(x,u_genre)
        staff_similarity=staff_compare(x,u_cast,u_crew)
        company_similarity=company_compare(x,u_company)
        language_similarity=language_compare(x,u_spoken_languages)
        keyword_similarity=keyword_compare(x,u_keywords)
        #权重部分
        similarity_score=(3*genre_similarity+1.5*staff_similarity+company_similarity+2*language_similarity+keyword_similarity)
        x.recommend_score=similarity_score*(x.rate_average if x.rate_count>500 else x.rate_average-((500-x.rate_count/500)*2))+x.popularity/50

    all_movies.sort(key=lambda x:x.recommend_score, reverse=True)
    recommend_list=[]
    for x in range(10):
        recommend_list.append(all_movies[x].ID)
    return recommend_list

input_json = js.loads(input())
import sys
sys.stderr.write(js.dumps(input_json))
print(recommendation(input_json))
