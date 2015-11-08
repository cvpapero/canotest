#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
正準相関分析
cca.py
'''

import numpy as np
import scipy as sp
from scipy import linalg as LA
from scipy import stats as ST
from scipy.spatial import distance as DIST


def cca(X, Y):
    '''
    正準相関分析
    http://en.wikipedia.org/wiki/Canonical_correlation
    '''    
    n, p = X.shape
    n, q = Y.shape

    # zero mean
    #X = X - X.mean(axis=0)
    #Y = Y - Y.mean(axis=0)
    X = ST.zscore(X, axis=0)
    Y = ST.zscore(Y, axis=0)

    print "mean:"
    print "X:"+str(X)
    print "Y:"+str(Y)
    print "X.mean:"+str(X.mean(axis=0))
    print "Y.mean:"+str(Y.mean(axis=0))
    print "X var:"+str(np.var(X))
    print "X var:"+str(np.var(Y))

    # covariances
    S = np.cov(X.T, Y.T, bias=1)
    print "cov:"
    print "S:"
    print str(S)

    # S = np.corrcoef(X.T, Y.T)
    SXX = S[:p,:p]
    SYY = S[p:,p:]
    SXY = S[:p,p:]
    SYX = S[p:,:p]
    print "SXX:"+str(SXX)
    print "SYY:"+str(SYY)
    print "SXY:"+str(SXY)
    print "SYX:"+str(SYX)

    # 
    sqx = LA.sqrtm(LA.inv(SXX)) # SXX^(-1/2)
    sqy = LA.sqrtm(LA.inv(SYY)) # SYY^(-1/2)
    #M = np.dot(np.dot(sqx, SXY), sqy.T) # SXX^(-1/2) * SXY * SYY^(-T/2)
    M = np.dot(SXY, SXY.T)
    A, s, Bh = LA.svd(M, full_matrices=False)
    B = Bh.T

    U = np.dot(np.dot(A.T, sqx), X.T).T
    V = np.dot(np.dot(B.T, sqy), Y.T).T

    print "M:"+str(M)
    print "s:"+str(s)
    print "A:"+str(A)
    print "B:"+str(B)
    print "U:"+str(U)
    print "V:"+str(V)

    return s, A, B, U, V


def gaussian_kernel(x, y, var=1.0):
    return np.exp(-np.linalg.norm(x - y) ** 2 / (2 * var))

def polynomial_kernel(x, y, c=1.0, d=2.0):
    return (np.dot(x, y) + c) ** d

def kcca(X, Y, kernel_x=gaussian_kernel, kernel_y=gaussian_kernel, eta=1.0):
    '''
    カーネル正準相関分析
    http://staff.aist.go.jp/s.akaho/papers/ibis00.pdf
    '''
    n, p = X.shape
    n, q = Y.shape
    X = ST.zscore(X, axis=0)
    Y = ST.zscore(Y, axis=0)

    Kx = DIST.squareform(DIST.pdist(X, kernel_x))
    Ky = DIST.squareform(DIST.pdist(Y, kernel_y))
    J = np.eye(n) - np.ones((n, n)) / n
    M = np.dot(np.dot(Kx.T, J), Ky) / n
    L = np.dot(np.dot(Kx.T, J), Kx) / n + eta * Kx
    N = np.dot(np.dot(Ky.T, J), Ky) / n + eta * Ky

    sqx = LA.sqrtm(LA.inv(L))
    sqy = LA.sqrtm(LA.inv(N))

    a = np.dot(np.dot(sqx, M), sqy.T)
    A, s, Bh = LA.svd(a, full_matrices=False)
    B = Bh.T

    # U = np.dot(np.dot(A.T, sqx), X).T
    # V = np.dot(np.dot(B.T, sqy), Y).T


    #print "M:"+str(M)
    print "s:"+str(s)
    print "A:"+str(A)
    print "B:"+str(B)


    return s, A, B


def get_data_1():
    X = np.array([[2,1],[1,2],[0,0],[-1,-2],[-2,-1]])
    Y = np.array([[2,2],[-1,-1],[0,0],[-2,1],[1,-2]])
    return X, Y

def get_data_2():
    n = 100
    theta = (np.random.rand(n) - 0.5) * np.pi
    x1 = np.sin(theta)
    x2 = np.sin(3 * theta)
    X = np.vstack([x1, x2]).T + np.random.randn(n, 2) * .05
    y1 = np.exp(theta) * np.cos(2 * theta)
    y2 = np.exp(theta) * np.sin(2 * theta)
    Y = np.vstack([y1, y2]).T + np.random.randn(n, 2) * .05
    return X, Y

def get_data_3():
    X = np.array([[73,57],[74,59],[86,63],[74,59],[80,60],[78,59],[86,61],[82,59],[87,64],[80,59]])
    Y = np.array([[61,48],[70,48],[79,52],[65,48],[55,42],[85,58],[57,48],[83,52],[70,52],[75,52]])
    return X, Y

def get_data_4():
    x1 = [[2,5,7,9,8,4,2,6,3,6],[3,4,6,8,5,3,3,5,4,7]]
    x2 = [[4,6,8,8,7,2,3,7,5,8],[3,3,5,9,6,5,4,7,4,6]]
    X = np.matrix(x1).T
    Y = np.matrix(x2).T
    print "X:"+str(X)
    print "Y:"+str(Y)
    return X, Y

def get_data_5():
    x1 = [[168.5, 182.6, 168.5, 182.6, 177.9, 154.4, 187.3, 173.2, 187.3, 173.2],
          [57.4, 85.4, 68.6, 85.4, 68.6, 51.8, 85.4, 57.4, 91.0, 68.6],
          [83.4, 98.9, 86.5, 98.9, 92.7, 80.3, 98.9, 86.5, 98.9, 92.7],
          [86.9, 93.4, 94.7, 89.5, 92.1, 85.6, 94.7, 94.7, 89.5, 92.1]]

    x2 = [[5.8, 6.8, 6.1, 7.2, 6.5, 5.1, 7.2, 6.1, 7.5, 6.1],
          [346, 412, 401, 357, 379, 335, 412, 423, 357, 379],
          [25.6, 33.2, 35.1, 29.4, 31.3, 23.7, 37.0, 35.1, 27.5, 31.3]]

    X = np.matrix(x1).T
    Y = np.matrix(x2).T
    #print "X:"+str(X)
    #print "Y:"+str(Y)
    return X, Y

def test_cca():
    #X, Y = get_data_1()
    #print "X:"+str(X)
    #print "Y:"+str(Y)
    #cca(X, Y)
    
    X, Y = get_data_5()
    print "X:"+str(X)
    print "Y:"+str(Y)
    cca(X, Y)


def test_kcca():
    X, Y = get_data_3()
    kcca(X, Y)
    #X, Y = get_data_2()
    #kcca(X, Y)

if __name__ == '__main__':
    test_cca()
    #test_kcca()
