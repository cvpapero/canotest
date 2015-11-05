#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from numpy.linalg import lstsq,eig
from numpy import cov,dot,arange,c_
import numpy as np    

def cca(x_tn,y_tm):
    x_tn = x_tn-x_tn.mean(axis=0)
    y_tm = y_tm-y_tm.mean(axis=0)
    N = x_tn.shape[1]
    M = y_tm.shape[1]
    xy_tq = c_[x_tn,y_tm]
    cqq = cov(xy_tq,rowvar=0)
    cxx = cqq[:N,:N]
    cxy = cqq[:N,N:(N+M)]
    cyx = cqq[N:(N+M),:N]
    cyy = cqq[N:(N+M),N:(N+M)]
    
    K = min(N,M)
    
    xldivy = lstsq(cxx,cxy)[0]
    yldivx = lstsq(cyy,cyx)[0]
    print xldivy
    print dot(np.linalg.inv(cxx),cxy)
    _,vecs = eig(dot(xldivy,yldivx))
    a_nk = vecs[:,:K]
    #print normr(vecs.T)
    b_mk = dot(yldivx,a_nk)
    
    u_tk = dot(x_tn,a_nk)
    v_tk = dot(y_tm,b_mk)
    
    return a_nk,b_mk,u_tk,v_tk
    
def normr(a):
    return a/np.sqrt((a**2).sum(axis=1))[:,None]

def test_cca():

    #x_tn = np.matrix([[73,74,86,74,80,78,86,82,87,80],[57,59,63,59,60,59,61,59,64,59]]).T
    #y_tm = np.matrix([[61,70,79,65,55,85,57,83,70,75],[48,48,52,48,42,58,48,52,52,52]]).T


    x_tn = np.matrix([[168.5, 182.6, 168.5, 182.6, 177.9, 154.4, 187.3, 173.2, 187.3, 173.2],[57.4, 85.4, 68.6, 85.4, 68.6, 51.8, 85.4, 57.4, 91.0, 68.6],[83.4, 98.9, 86.5, 98.9, 92.7, 80.3, 98.9, 86.5, 98.9, 92.7],[86.9, 93.4, 94.7, 89.5, 92.1, 85.6, 94.7, 94.7, 89.5, 92.1]]).T
    y_tm = np.matrix([[5.8, 6.8, 6.1, 7.2, 6.5, 5.1, 7.2, 6.1, 7.5, 6.1],[346, 412, 401, 357, 379, 335, 412, 423, 357, 379],[25.6, 33.2, 35.1, 29.4, 31.3, 23.7, 37.0, 35.1, 27.5, 31.3]]).T

    #print(x_tn)
    #print(y_tm)
    a,b,u,v = cca(x_tn,y_tm)
    print("a")
    print normr(a)
    print a
    print("b")
    print normr(b)
    print("u")
    print u
    print("v")
    print v

    
if __name__ == "__main__":
    test_cca()
