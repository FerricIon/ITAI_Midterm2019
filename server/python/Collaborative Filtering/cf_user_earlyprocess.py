import csv
import json as js
def csv_to_mur():
    with open('ratingsg.csv','r') as mfile:
        umr=csv.reader(mfile)
        a=0
        j=0
        data={}
        for line in umr:
            if j==1 and line[0]!=umark:
                break
            if line[1] not in data.keys():
                data[line[1]]={}
            data[line[1]][line[0]]=float(line[2])
            a+=1
            if a==1000000:
                j=1
                umark=line[0]
        with open('cf_userInit.json','w') as out:
            out.write(js.dumps(data))
def csv_to_ave():
    with open('ratingsg.csv','r') as mfile:
        umr=csv.reader(mfile)
        a=0
        j=0
        count={}
        total={}
        ave={}
        for line in umr:
            if j==1 and line[0]!=umark:
                break
            if line[0] not in count.keys():
                count[line[0]]=0
            if line[0] not in total.keys():
                total[line[0]]=0
            count[line[0]]+=1
            total[line[0]]+=float(line[2])
            a+=1
            if a==1000000:
                j=1
                umark=line[0]
        for u in count.keys():
            ave[u]=round(total[u]/count[u],5)
        with open('cf_userAve.json','w') as out:
            out.write(js.dumps(ave))
csv_to_ave()