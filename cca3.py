#!/usr/bin/python
# -*- coding: utf-8 -*-


#標準化する

import sys
import math
import json
import numpy as np
import scipy as sp
from scipy import linalg as LA
from scipy import stats as ST
from scipy.spatial import distance as DIST

from sklearn.cross_decomposition import CCA

class CanCorr():

    def __init__(self):
        self.winSize = 3

        self.jsonInput()
        self.dataAlig()
        self.dataNorm()
        self.canoniCorr()

    #データのインプット(from json)
    def jsonInput(self):
        f = open('testdata3.json', 'r');
        jsonData = json.load(f)
        #print json.dumps(jsonData, sort_keys = True, indent = 4)
        f.close()

        self.jdatas = []
        for user in jsonData:
            #angle
            datas = []
            self.dataRow = len(user["datas"])

            for j in range(self.dataRow):
                datas.append(user["datas"][j]["data"])

            self.jdatas.append(datas)
        #print "jdatas:"
        #print(self.jdatas)

    #データの整頓(winsize分だけ並べる)
    def dataAlig(self):

        self.X = []
        self.Y = []

        self.range = self.dataRow-self.winSize+1

        for i in range(self.range):
            data = []
            for w in range(self.winSize):
                #data.extend(self.jdatas[0][w+i])
                data.extend(self.scale(self.jdatas[0][w+i]))
            self.X.append(data)
       
        for i in range(self.range):
            data = []
            for w in range(self.winSize):
                #data.extend(self.jdatas[1][w+i])
                data.extend(self.scale(self.jdatas[1][w+i]))
            self.Y.append(data)
   
        print "dataAlig_X:"
        for i in range(len(self.X)):
            print(self.X[i])
        print("---")

        print "dataAlig_Y:"
        for i in range(len(self.Y)):
            print(self.Y[i])
        print("---")
        

    #平均=0
    def scale(self, arr):
        dst = []
        m = np.mean(arr)
        #s = np.std(arr)
        #f s != 0.0:
        #st = np.array([(arr[i] - m)/s for i in range(len(arr))])
        dst = np.array([(arr[i] - m) for i in range(len(arr))])
        #print("mean:"+str(np.mean(dst)))
        #print("std:"+str(np.std(dst)))
        return dst

    
    def dataNorm(self):
        SXX = np.cov(self.X)
        U, l, Ut = LA.svd(SXX, full_matrices=True) 
        H = np.dot(LA.sqrtm(LA.inv(np.diag(l))),Ut)
        self.nX = np.dot(H,self.X)

        #print np.cov(self.nX)
        #print "mean:"
        #print np.mean(self.nX)

        SYY = np.cov(self.Y)
        U, l, Ut = LA.svd(SYY, full_matrices=True) 
        H = np.dot(LA.sqrtm(LA.inv(np.diag(l))),Ut)
        #print "H"
        #print H
        self.nY = np.dot(H,self.Y)
        #print np.cov(self.nY)

        print "dataNorm_X:"
        for i in range(len(self.nX)):
            print(self.nX[i])
        print("---")

        print "dataNorm_Y:"
        for i in range(len(self.nY)):
            print(self.nY[i])
        print("---")

    #正準相関
    def canoniCorr(self):

        S = np.cov(self.nX, self.nY)

        print "cov:"
        print S

        p,q = S.shape
        p = p/2
        SXX = S[:p,:p]
        SYY = S[p:,p:]
        SXY = S[:p,p:]
        SYX = S[p:,:p]
        SS = np.dot(SXY,SXY.T)
        print "SXX:"
        print SXX
        print "SYY:"
        print SYY
        #print "SXY:"+str(SXY)
        #print "SYX:"+str(SYX)
        
        print "SxySyx:"
        print SS

        mwx, s, B = LA.svd(SS, full_matrices=True)
        #s, mwx = LA.eig(SS)

        print "mwx:"
        print mwx
        print "wxt*sxx*wx"
        print np.dot(np.dot(mwx[:,0:1].T,SXX),mwx[:,0:1])

        print "s:"
        print np.diag(s)

        p,q = mwx.shape
        
        mwy = np.dot(np.dot(SYX,mwx),np.diag(1/np.sqrt(s)))

        print "mwy:"
        print mwy
        print "wyt*syy*wy"
        print np.dot(np.dot(mwy[:,0:1].T,SYY),mwy[:,0:1])

        #cca = CCA(n_components=1)
        #print cca.fit(self.nX, self.nY)
        #X_c, Y_c = cca.fit_transform(self.nX, self.nY)

        #print "X_c:"
        #print X_c
        #print "Y_c:"
        #print Y_c
        

        '''
        #adatasm = np.matrix(self.adatas).T
        #print adatasm
        #fdata = adatasm[:,0:colSize/2]
        #fdata = adatasm[:,:self.range]
        #gdata = adatasm[:,self.range:]

        #print fdata
        #print gdata

        f = np.dot(self.nX, mwx)
        g = np.dot(self.nY, mwy)

        #print f
        #print g

        #print np.corrcoef(fdata[:,0:1].T,f[:,0:1].T)
        #print np.corrcoef(fdata[:,1:2].T,f[:,0:1].T)

        fcorr = np.corrcoef(self.nX.T,f.T)
        gcorr = np.corrcoef(self.nY.T,g.T)

        #print fcorr

        rf = fcorr[:self.range,self.range:self.range+1]
        rg = gcorr[:self.range,self.range:self.range+1]
        
        #rf = rf.T
        #rg = rg.T
        #正準構造ベクトル
        print "rf:"
        print rf
        print "rg:"
        print rg
        
        #寄与率
        fcrat = np.dot(rf.T,rf)/self.range
        gcrat = np.dot(rg.T,rg)/self.range
        
        print "contribution ratio:"
        print fcrat
        print gcrat

        #冗長率
        fred = np.corrcoef(fdata.T,g.T)
        gred = np.corrcoef(gdata.T,f.T)

        fred = fred[:self.range,self.range:self.range+1]
        gred = gred[:self.range,self.range:self.range+1]

        frrat = np.dot(fred.T,fred)/self.range
        grrat = np.dot(gred.T,gred)/self.range
        print "radundancy ratio:"
        print frrat
        print grrat

    '''

    def kCanoniCorr(self):
        pass

def main():
    cancorr = CanCorr()
        

if __name__=='__main__':
    main()
