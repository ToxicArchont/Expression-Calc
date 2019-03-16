# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 17:48:57 2019

@author: anton
"""
import re


#line=''
possacts={'+':1,'-':2,'*':3,'/':4}

def ret(line):
    return line

def calculate(a,b,act):
        if possacts[act]==1:
            return a+b
        elif possacts[act]==2:
            return a-b
        elif possacts[act]==3:
            return a*b    
        else:
            return a/b

def execute(query):
    '''variables'''
    global possacts
    
    i=0
    nums={}
    actions={}
    flag=0
    prevdivind=0
    divind=-1
    addind=0
    # poluchenie informatsii / data fetch
    i=0
    query=query.strip('(')
    query=query.strip(')')
    tesu=query.split('-')
    if len(tesu)==2 and tesu[0]=='' and '+' not in tesu[1] and '/' not in tesu[1] and '*' not in tesu[1] : 
        return -1*int(query.split('-')[1])
    while i !=len(query):
        symb=query[i]
        if symb in possacts.keys():
            prevdivind=divind
            divind=i
            actions[addind]=actions.get(symb,'')+symb
            sodes=query[prevdivind+1:divind].strip('(')
            sodes=sodes.strip(')')
            if sodes=='' and len(actions)==0:
                del actions[len(nums)]
                addind-=1
            elif sodes=='' and len(actions)!=0:
                del actions[addind]
                flag=addind
                addind-=1
            elif sodes!='':    
                if query[0]=='-' and query.count('-')<2:
                    nums[addind]=nums.get(symb,0)-float(sodes)
                else:
                    nums[addind]=nums.get(symb,0)+float(sodes)
                if flag!=0:
                    nums[addind]=nums[addind]*-1
                    flag=0
            addind+=1
        
        i+=1
    if flag==0:
        nums[addind]=nums.get(symb,0)+float(query[divind+1:len(query)])
    else:
        nums[addind]=nums.get(symb,0)-float(query[divind+1:len(query)])
    if query[0]=='-' and nums[0]>0:
        nums[0]=-1*nums[0]
    # vychislenie umnozheniya i deleniya
    addind=0
    while '*' in actions.values() or '/' in actions.values(): 
        if possacts[actions[addind]]==3 or possacts[actions[addind]]==4:
            if addind in nums.keys():
                temp1=calculate(nums[addind],nums[addind+1],actions[addind])
            else:
                addind+=1
                temp1=calculate(nums[addind],nums[addind+1],actions[addind])
            del actions[addind]
            del nums[addind]
            nums[addind+1]=temp1
        addind+=1
    #vychislenie summy rezultatov pred. punkta
    res1n=list(nums.values())
    res2a=list(actions.values())
    addind=0
    if query[0]=='-':
        if res1n[0]>0 and query.count('-')<2:
            res1n[0]=-1*res1n[0]
        if len(actions)>1 and len(res2a)>1: 
            if query.count('-')>1:
                pass
            else:
                del res2a[0]
                del actions[0]
    for i in range(len(actions)):
        temp1=calculate(res1n[addind],res1n[addind+1],res2a[addind])
        res1n[addind+1]=temp1
        del res1n[addind]
        del res2a[addind]    
    #print('Result:',temp1)
    i=0
    return temp1

def parser(a):
    def opcnt(line):
        return(line.count('('))
    def clcnt(line):
        return(line.count(')'))
    opind=[]#indexy otkrytyx skobok
    clind=[]#indexy zakrytyx skobok
    pairs=[]
    i,j=0,0
    if '(' in a:
        for k in range(len(a)):
            if a[k]=='(':
                opind.append(k)
            elif a[k]==')':
                clind.append(k)
        length=len(opind)
        for i in range(length):
            while j<length:
                if opcnt(a[opind[i]:clind[j]+1])==clcnt(a[opind[i]:clind[j]+1]):
                    pairs.append((clind[j],opind[i],clind[j]))
                    del clind[j]
                    j=0
                    break
                j+=1
        pairs.sort()          
        #print(pairs)
        return (pairs)
    return []

def result(line):
    #line=input('Hey, please input expression below:\n')
    b=parser(line)
    #vychislenie i zamena skobok
    while len(b)>0:
        pre=line[0:b[0][1]] 
        #print(pre)
        aft=line[b[0][2]+1:len(line)]
        #print(aft)
        bra=line[b[0][1]+1:b[0][2]]
        #print(bra)
        bra=str(execute(bra))
        #print(bra)
        line=pre+bra+aft
        del b[0]
        bra=''
        b=parser(line)
    #print(line)
    
    #ispravlenie oshibok pri s'chityvanii
    nomera=re.split('[-+*/]',ret(line))
    while '' in nomera:
        nomera[nomera.index('')+1]='-'+nomera[nomera.index('')+1]
        del nomera[nomera.index('')]
    for i in range(len(nomera)):
        nomera[i]=float(nomera[i])
    deistv=re.split('[^-+*/]',ret(line))
    while '' in deistv:
        deistv.remove('')
    ind=0
    while '*-' in deistv or '/-' in deistv or '+-' in deistv or '--' in deistv:
        if len(deistv[ind])>1:
            deistv[ind]=deistv[ind][0]
        ind+=1
    ind=0
    if nomera[0]<0:
        del deistv[0]
    #vychislenie * i / v samom vyrazhenii
    while '*' in deistv or '/' in deistv:
        if possacts[deistv[ind]]==3 or possacts[deistv[ind]]==4:
            nomera[ind]=calculate(nomera[ind],nomera[ind+1],deistv[ind])
            del nomera[ind+1]
            del deistv[ind]
            ind-=1
        ind+=1    
    ind=0
    #ostalniye vychisleniya
    while len(deistv)>0:
        if len(deistv)==1 and ind!=0:
            ind-=1
        nomera[ind]=calculate(ret(nomera[ind]),ret(nomera[ind+1]),deistv[ind])
        del nomera[ind+1]
        del deistv[ind]
        ind+=1
    print()
    #vyvod rezul'tata
    if len(nomera)>1:
        deistv=re.split('[^-+*/]',ret(line))
        while '' in deistv:
            deistv.remove('')
        resu=calculate(nomera[0],nomera[1],deistv[0])
        print('Result:',resu)
        return resu
    else:
        print('Result:',nomera[0])
        return nomera[0]
    return ''
#result('((11-23)/(-4))*2')
'''
b=parser(line)
#vychislenie i zamena skobok
while len(b)>0:
    pre=line[0:b[0][1]] 
    print(pre)
    aft=line[b[0][2]+1:len(line)]
    print(aft)
    bra=line[b[0][1]+1:b[0][2]]
    print(bra)
    bra=str(execute(bra))
    print(bra)
    line=pre+bra+aft
    del b[0]
    bra=''
    b=parser(line)
print(line)

#ispravlenie oshibok pri s'chityvanii
nomera=re.split('[-+*/]',ret(line))
while '' in nomera:
    nomera[nomera.index('')+1]='-'+nomera[nomera.index('')+1]
    del nomera[nomera.index('')]
for i in range(len(nomera)):
    nomera[i]=float(nomera[i])
deistv=re.split('[^-+*/]',ret(line))
while '' in deistv:
    deistv.remove('')
ind=0
while '*-' in deistv or '/-' in deistv or '+-' in deistv or '--' in deistv:
    if len(deistv[ind])>1:
        deistv[ind]=deistv[ind][0]
    ind+=1
ind=0
if nomera[0]<0:
    del deistv[0]
#vychislenie * i / v samom vyrazhenii
while '*' in deistv or '/' in deistv:
    if possacts[deistv[ind]]==3 or possacts[deistv[ind]]==4:
        nomera[ind]=calculate(nomera[ind],nomera[ind+1],deistv[ind])
        del nomera[ind+1]
        del deistv[ind]
        ind-=1
    ind+=1    
ind=0
#ostalniye vychisleniya
while len(deistv)>0:
    if len(deistv)==1 and ind!=0:
        ind-=1
    nomera[ind]=calculate(ret(nomera[ind]),ret(nomera[ind+1]),deistv[ind])
    del nomera[ind+1]
    del deistv[ind]
    ind+=1
print()
#vyvod rezul'tata
if len(nomera)>1:
    deistv=re.split('[^-+*/]',ret(line))
    while '' in deistv:
        deistv.remove('')
    print('Result:',calculate(nomera[0],nomera[1],deistv[0]))
else:
    print('Result:',nomera[0])
'''
