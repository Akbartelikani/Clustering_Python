import math
import numpy as np
import pandas as pd
def readfile(Year,Key,Name):           
    Company_Name=[]
    Inf_Company=[]    
    for i in range(len(Name)):
        FileName=NonEmpty_Comp[i]
        df = pd.read_csv(FileName+'.csv', skiprows =[0,1])       
        File_array= np.array(df)
        if len(File_array)<2:
            input()
        Fields_List1=[FileName,0,0,0,0,0,0,0]
        Fields_List2=[0,0,0,0,0,0,0]
        for j in range(len(File_array)):
            for k in range(1,len(Key)):
                if File_array[j][0]==Key[k]:
                   Switch=1
                   tel=str(File_array[j][Year]).split(',')
                   if len(tel)>1:
                       a=float(tel[0])*1000+float(tel[1])
                   else:
                       a=float(tel[0])
                   if math.isnan(a):
                       a=0
                       Switch=0
                   Fields_List1[k]=a
                   Fields_List2[k-1]=a
        if Switch!=0:
            Company_Name.append(Fields_List1[0])
            Inf_Company.append(Fields_List2)
    Company_Name=np.array(Company_Name)
    Inf_Company=np.array(Inf_Company)   
    return Company_Name,Inf_Company
def eucl_dist(a, b, axis=1): #euclidean distance betwen a,b
    return np.linalg.norm(a - b, axis=axis)   
def k_mean(x, k):
    #initalizing cluster variable
    cluster = np.zeros(x.shape[0]) #creat cluster 0 (x.shape[0]==no. of x row)    
    # calculation min and max for every dimension of data
    minv = np.min(x,axis=0)   # x: min of each roww
    maxv = np.max(x,axis=0)   # x: max of each roww    
    # initalizing centroids of k clusters
    center = np.zeros((k, x.shape[1]))
    for i in range(k):       
        for j in range(x.shape[1]):
            center[i,j] = np.random.randint(minv[j], maxv[j])    
    # assigining zeros to old centroids value
    center_old = np.zeros(center.shape)   #creat center 0 (k**no. of x colou         
    # initial error
    err = eucl_dist(center, center_old, None) #euclidean distance of all elements          
    while err != 0:      
        # calculatin distance of data points from centroids and assiging min distance cluster centroid as data point cluster
        for i in range(len(x)):
            distances = eucl_dist(x[i], center)           
            clust = np.argmin(distances)           
            cluster[i] = clust        
        # changing old centroids value
        center_old = np.copy(center)        
        # Finding the new centroids by taking the average value
        points=[]
        for i in range(k):            
            temp = []
            for j in range(len(x)):
                if cluster[j] == i:
                    temp.append(x[j])
            points.append(temp)                   
            if temp:
                center[i] = np.mean(temp, axis=0)        
        # calculation difference between new centroid and old centroid values
        err = eucl_dist(center, center_old, None)        
    # calculation total difference between cluster centroids and cluster data points
    errort=0
    error=[]
    for i in range(k):
        temp=0
        d = [eucl_dist(x[j],center[i],None) for j in range(len(x)) if cluster[j] == i]
        temp+= np.sum(d)
        errort+=temp
        error.append(temp)
    errt=errort/len(x)        
    return center,cluster,points,error,errt
# MAIN:
#READ AND MODIFY RECORDS    
#2009-09 2010-09 2011-09	2012-09	2013-09	2014-09	2015-09	2016-09	2017-09	2018-09	TTM
        # 1          2        3        4       5       6       7      8       9       10
#key=['co name','Revenue USD Mil','Shares Mil','Free Cash Flow USD Mil','Long-Term Debt',	'SG&A',	'Net Margin %',	'Free Cash Flow/Sales %']
name=[]    
file = open('TOTALNEW.txt',"r")
for line in file:
    b=line.split('\n')          
    name.append(b[0])  
file.close()
print("Number of total records",len(name))         
Company_Name=[]
Inf_Company=[]
NonEmpty_Comp=[]          
for i in range(len(name)):
    File_Name=name[i]
    file = open(File_Name+'.csv',"r")
    b=file.readline()
    b=file.readline()
    if len(b)<2:
        a=0
    else:    
        NonEmpty_Comp.append(File_Name)
    file.close()
print(len(name)-len(NonEmpty_Comp),'Files are empty and removed')    
print('Numberof not empty records',len(NonEmpty_Comp))
key=['Co. Name','Revenue USD Mil','Shares Mil','Free Cash Flow USD Mil','Book Value Per Share * USD',	'Operating Income USD Mil',	'Net Margin %',	'Free Cash Flow/Sales %']
print('Choosed financial variables Field:')
key1=list(key)
del key1[0]
print(key1)
Missing_Field=[] 
for i in range(len(NonEmpty_Comp)):
    Switch=1
    FileName=NonEmpty_Comp[i]
    df = pd.read_csv(FileName+'.csv', skiprows =[0,1])       
    File_array= np.array(df)    
    for j in range(len(File_array)):
        for k in range(1,len(key)):            
            if File_array[j][0]==key[k]:
               for y in range (5,8):    
                   Temp_array=str(File_array[j][y]).split(',')
                   if len(Temp_array)>1:
                       a=float(Temp_array[0])*1000+float(Temp_array[1])
                   else:
                       a=float(Temp_array[0])
                   if math.isnan(a):
                       Switch=0
    if Switch==1:
        Missing_Field.append(File_Name)
print(len(NonEmpty_Comp)-len(Missing_Field),'Files with missing values, which are removed')        
print('Number of records with complete fields',len(Missing_Field))        
#START===============================================
tr=[]
for it in range(5):                      
    com=[]        
    for k in range (2,9):        
        u=[]        
        for i in range(3):
            Company_Name,Inf_Company=readfile(y,key,Missing_Field)
            Company_Name= np.array(Company_Name)
            Inf_Company=np.array(Inf_Company)       
            center,cluster,points,error,errt = k_mean(Inf_Company,k)
            pointsM=[]
            for i in range(k):    
                temp = []
                for j in range(len(Inf_Company)):
                    if cluster[j] == i:
                        temp.append(Company_Name[j])
                pointsM.append(temp)
            u.append(pointsM)
    #============================================       
        print('Common companies in clusters at #Iteration',it+1,':')       
        for i in range(3):        
            temp=[]
            for i0 in range (k):                                   
                for i1 in range(k):                       
                    for i2 in range(k):
                       a=u[0][i0] 
                       b=set(u[1][i1]) 
                       c=(b.intersection(a)) 
                       d=set(u[2][i2])
                       e=(c.intersection(d))
                       if len(e)>1:
                           temp.append(e)
                           #print('k=',k,':\n',e)
        print('k',k,'\n',temp)
        com.append(temp)
    #for i in range(len(com)):
        #print('\n k=',i+2,'\n',com[i])
    #==========================================================    
    print('Companies in same groups at #Iteration',it+1,':')
    con=0
    e1=[]
    for i0 in range(len(com[0])):
        for i1 in range (len(com[1])):
            for i2 in range (len(com[2])):
                for i3 in range (len(com[3])):
                    for i4 in range (len(com[4])):
                        for i5 in range (len(com[5])):
                            for i6 in range (len(com[6])):
                                e=(com[0][i0].intersection(com[1][i1]))
                                e=(e.intersection(com[1][i1]))
                                e=(e.intersection(com[2][i2]))
                                e=(e.intersection(com[3][i3]))
                                e=(e.intersection(com[4][i4]))
                                e=(e.intersection(com[5][i5]))
                                e=(e.intersection(com[6][i6]))
                                if len(e)>1:
                                    con=con+1
                                    e=list(e)
                                    e.sort() 
                                    print('Group',con,'#Iteration',it+1,':')
                                    print("Number of members ",len(e),'\n',e)
                                    e1.append(e)
    tr.append(e1)
def shar(y):
    temp1a=[]
    temp1b=[]
    temp1c=[]
    temp1d=[]
    temp1e=[]
    g=set(y[0]).union(set(y[1]))
    g=g.union(set(y[2]))
    g=g.union(set(y[3]))
    g=g.union(set(y[4]))
    gg=list(g)
    ya=[y[0],y[1],y[2],y[3]]
    yb=[y[0],y[1],y[2],y[4]]
    yc=[y[0],y[1],y[3],y[4]]
    yd=[y[0],y[2],y[3],y[4]]
    ye=[y[1],y[2],y[3],y[4]]
    for j in range(len(g)):
        co=0
        for i in range(len(ya)):                                    
            if gg[j] in ya[i]:
                co=co+1
        if co==4:
            
            temp1a.append(gg[j])
        co=0    
        for i in range(len(yb)):                                    
            if gg[j] in yb[i]:
                co=co+1
        if co==4:
            temp1b.append(gg[j])
        co=0    
        for i in range(len(yc)):                                    
            if gg[j] in yc[i]:
                co=co+1
        if co==4:
            temp1c.append(gg[j])
        co=0    
        for i in range(len(yd)):                                    
            if gg[j] in yd[i]:
                co=co+1
        if co==4:
            temp1d.append(gg[j])
        co=0    
        for i in range(len(ye)):                                    
            if gg[j] in ye[i]:
                co=co+1
        if co==4:
            temp1e.append(gg[j])    
    Fields_List1=[temp1a,temp1b,temp1c,temp1d,temp1e ]    
    return Fields_List1       
#print(tr)   
print('==========================')
print('Companies in same group at 3-year and all cluster and 80% in 5 iterations:')  
con=0
Fields_List2=[]    
for i0 in range(len(tr[0])):
    for i1 in range (len(tr[1])):
        for i2 in range (len(tr[2])):
            for i3 in range (len(tr[3])):
                for i4 in range (len(tr[4])):
                    y0=tr[0][i0]
                    y1=tr[1][i1]
                    y2=tr[2][i2]
                    y3=tr[3][i3]
                    y4=tr[4][i4]
                    y=[y0,y1,y2,y3,y4]
                    temp=shar(y)
                    for i in range(len(temp)):
                        if len(temp[i])>1:                          
                            temps=np.sort(temp[i])
                            temps=list(temps)
                            Fields_List2.append(temps) 
for i in range(len(Fields_List2)):
    k=i+1
    for j in range(k,len(Fields_List2)):
        a=set(Fields_List2[i])
        b=set(Fields_List2[j])
        c=b.intersection(a)
        d=min(len(a),len(b))
        if len(c)==d and len(c)>0:
            if len(b)>len(a):
                Fields_List2[i]=Fields_List2[j]
            Fields_List2[j]=[]
co=0        
for i in range(len(Fields_List2)):
    if Fields_List2[i]!=[]:
        co=co+1
        print('#Group',co)
        print("Number of members",len(Fields_List2[i]))      
        print(Fields_List2[i])