import pandas
import random
import numpy as np
from functools import reduce
from operator import mul
from fractions import Fraction
from math import sqrt
import hashlib


def nCk(n,k):
    return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

def uniformFitnessGranular(oriDist,eps2=0.1):

    if not(oriDist):
        return(0)
    p=[]
    for i in range(len(oriDist[0])):
        p.append([item[i] for item in oriDist])
    accumulative=0
    for dimension in p:
        domain=np.unique(dimension)
        #The numer of samples come from lemma 5 of collision-based testers are optimal for uniformity and closeness
        s = 0
        for i in range(len(dimension)):
            s = s+ dimension[(i+1):len(dimension)].count(dimension[i])
        t= nCk(len(dimension),2)*(1+3/4*eps2)/len(domain)
        if(s==0):
            accumulative=accumulative+1
        else:
            accumulative=accumulative+1-1/(t/s+1)
    return accumulative/len(p)


def uniformFitness(oriDist,eps2=0.1):

    if not(oriDist):
        return(0)
    noDupes = []
    [noDupes.append(i) for i in oriDist if not noDupes.count(i)]
    #dist = pandas.DataFrame(oriDist)
    #print(dist)
    #domain=np.unique(dist,axis=0)
    domain=noDupes
    #The numer of samples come from lemma 5 of collision-based testers are optimal for uniformity and closeness
    s = 0
    for i in range(len(oriDist)):
        s = s+ oriDist[(i+1):len(oriDist)].count(oriDist[i])
    t= nCk(len(oriDist),2)*(1+3/4*eps2)/len(domain)
    if(s==0):
        return(1)
    return(1-1/(t/s+1))


#Instead of working directly with eps, due to all the operations are performed with eps^2, and the distance is calculated through this value, we pass this value directly
def uniformComparison(oriDist,eps2=0.1):

    if not(oriDist):
        print("Empty")
        return
    dist = pandas.DataFrame(oriDist)
    domain=np.unique(dist,axis=0)
    #The numer of samples come from lemma 5 of collision-based testers are optimal for uniformity and closeness
    expected= 6*sqrt(len(domain))/eps2
    if(len(oriDist) < expected):
        print("You need " + str(expected) + " samples")
    else:
        print("The domain lenght is: "+str(len(domain)))
    s = 0
    for i in range(len(oriDist)):
        s = s+ oriDist[(i+1):len(oriDist)].count(oriDist[i])
    t= nCk(len(oriDist),2)*(1+3/4*eps2)/len(domain)
    if(s>t):
        print("Fail")
        print(oriDist)
        print("s="+str(s))
        print("t="+str(t))
    else:
        print("Done")
        print("s="+str(s))
        print("t="+str(t))

def oldUniformComparison(oriDist,eps):
    dist = pandas.DataFrame(oriDist)
    dist1 = dist[0]
    domain=dist1.unique()
    dist2 = pandas.DataFrame([np.random.choice(domain) for i in range(len(dist1))])
    dist2 = dist2[0]
    c1 = 0
    for i in range(len(dist1)):
        c1 = c1+ sum(dist1[(i+1):len(dist1)]==dist1[i])
    c2 = 0
    for i in range(len(dist2)):
        c2 = c2+ sum(dist2[(i+1):len(dist2)]==dist2[i])
    c3 = 0
    for i in range(len(dist1)):
        c3 = c3+ sum(dist1[i]==dist2)
    Z= c1+c2 - (len(dist1)-1)/len(dist1)*c3
    t= nCk(len(dist1),2)*pow(eps,2)/2
    if(Z>t):
        print("Fail")
        print(dist1)
        print(dist2)
        print(1/Z)
    else:
        print("Done")
    print(c1)
    print(c2)
    print(c3)
    print(t)
    print(Z)

def probsComparison(oriDist,newDist,eps):
    dist = pandas.DataFrame(oriDist)
    dist1 = dist[0]
    domain=dist1.unique(axis=0)
    dist = pandas.DataFrame(newDist)
    dist2 = dist[0]
    c1 = 0
    for i in range(len(dist1)):
        c1 = c1+ sum(dist1[(i+1):len(dist1)]==dist1[i])
    c2 = 0
    for i in range(len(dist2)):
        c2 = c2+ sum(dist2[(i+1):len(dist2)]==dist2[i])
    c3 = 0
    for i in range(len(dist1)):
        c3 = c3+ sum(dist1[i]==dist2)
    Z= c1+c2 - (len(dist1)-1)/len(dist1)*c3
    t= nCk(len(dist1),2)*pow(eps,2)/2
    if(Z>t):
        print("Fail")
        print(dist1)
        print(dist2)
        print(1/Z)
    else:
        print("Done")
    print(c1)
    print(c2)
    print(c3)
    print(t)
    print(Z)
