#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import math
import json
import numpy as np
import scipy as sp
from scipy import linalg as LA
from scipy import stats as ST

class CanCorr():

    def __init__(self):
        self.winSize = 3

        self.jsonInput()
        self.dataAlig()
        self.canoniCorr()

    #データのインプット(from json)
    def jsonInput(self):
        f = open('testdata2.json', 'r');
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
        self.adatas = []
        self.range = self.dataRow-self.winSize+1

        for u in range(len(self.jdatas)):
            adata = []
            for i in range(self.range):
                data = []
                for w in range(self.winSize):
                    #data.extend(self.jdatas[u][w+i])
                    data.extend(self.scale(self.jdatas[u][w+i]))
                self.adatas.append(data)
          
        '''
        print "dataAlig:"
        for i in range(len(self.adatas)):
            print(self.adatas[i])
        print("---")
        '''

    #標準化
    def scale(self, arr):
        dst = []
        m = np.mean(arr)
        s = np.std(arr)
        if s != 0.0:
            dst = np.array([(arr[i] - m)/s for i in range(len(arr))])
        #print("mean:"+str(np.mean(dst)))
        #print("std:"+str(np.std(dst)))
        return dst

    #正準相関
    def canoniCorr(self):

        S = np.cov(self.adatas)

        print "cov:"
        print S

        p,q = S.shape
        p = p/2
        SXX = S[:p,:p]
        SYY = S[p:,p:]
        SXY = S[:p,p:]
        SYX = S[p:,:p]
        SS = np.dot(SXY,SYX)
        #print "SXX:"+str(SXX)
        #print "SYY:"+str(SYY)
        #print "SXY:"+str(SXY)
        #print "SYX:"+str(SYX)
        
        print "SxySyx:"
        print SS

        mwx, s, B = LA.svd(SS, full_matrices=True)

        print "mwx:"
        print mwx
        print "s:"
        print np.diag(s)

        p,q = mwx.shape
        
        mwy = np.dot(np.dot(SYX,mwx),np.diag(1/np.sqrt(s)))

        print "mwy:"
        print mwy
        adatasm = np.matrix(self.adatas).T
        #print adatasm
        #fdata = adatasm[:,0:colSize/2]
        fdata = adatasm[:,:self.range]
        gdata = adatasm[:,self.range:]

        #print fdata
        #print gdata

        f = np.dot(fdata, mwx)
        g = np.dot(fdata, mwy)

        #print f
        #print g

        #print np.corrcoef(fdata[:,0:1].T,f[:,0:1].T)
        #print np.corrcoef(fdata[:,1:2].T,f[:,0:1].T)

        fcorr = np.corrcoef(fdata.T,f.T)
        gcorr = np.corrcoef(gdata.T,g.T)

        print fcorr

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

def main():
    cancorr = CanCorr()
        

if __name__=='__main__':
    main()
