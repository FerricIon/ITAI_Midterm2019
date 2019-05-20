import json as js
file1=open('cf_userInit.json','r')
file2=open('cf_userAve.json','r')
mur=js.load(file1)
ave=js.load(file2)
file1.close()
file2.close()
data={}
a=0
for mid1 in mur.keys():
    for mid2 in mur.keys():
        if mid1<mid2:
            comUser=set(mur[mid1].keys()).intersection(mur[mid2].keys())
            a1=0
            a2=0
            a3=0
            for uid in comUser:
                a1+=(mur[mid1][uid]-ave[uid])*(mur[mid2][uid]-ave[uid])
                a2+=(mur[mid1][uid]-ave[uid])**2
                a3+=(mur[mid2][uid]-ave[uid])**2
            if mid1 not in data.keys():
                data[mid1]={}
            if mid2 not in data.keys():
                data[mid2]={}
            if a2==0 or a3==0:
                data[mid1][mid2]=0
                data[mid2][mid1]=0
            else:
                data[mid1][mid2]=round(a1/((a2*a3)**0.5),4)
                data[mid2][mid1]=round(a1/((a2*a3)**0.5),4)
            a+=1
            if not a%10000:
                print(a)
file3=open('cf_matrix_BasedonUser.json','w')
file3.write(js.dumps(data))
file3.close()