#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import math
import json
import numpy as np
import scipy as sp


class CanCorr():

    def __init__(self):
        self.winSize = 3

        self.jsonInput()
        self.dataAlignment()
        self.canoniCorr()

    def jsonInput(self):
        f = open('test1014.json', 'r');
        jsonData = json.load(f)
        #print json.dumps(jsonData, sort_keys = True, indent = 4)
        f.close()

        self.dataSize = len(jsonData[0]["datas"])
        print ("dataRow:"+str(self.dataSize))
        self.jdatas = []
        for user in jsonData:
            #angle
            datas = []
            for j in range(self.dataSize):
                datas.append(user["datas"][j]["data"])
            self.jdatas.append(datas)
        print(self.jdatas)
        #print(udatas[1][0][0])

    def dataAlignment(self):
        self.adatas = []
        self.range = self.dataSize-self.winSize+1
        for user in self.jdatas:
            adata = []
            for i in range(self.range):
                data = []
                for w in range(self.winSize):
                    #data.extend(user[w+i])
                    data.extend(self.scale(user[w+i]))
                self.adatas.append(data)
            #self.adatas.append(adata)
            
        for i in range(len(self.adatas)):
            print(self.adatas[i])
        print("---")
        #print(self.adatas[0][1])
        #print(self.adatas[0][2])
        #print(self.adatas[1][0])
        #print(self.adatas[1][1])
        #print(self.adatas[1][2])

    def scale(self, arr):
        dst = []
        m = np.mean(arr)
        s = np.std(arr)
        if s != 0.0:
            dst = np.array([(arr[i] - m)/s for i in range(len(arr))])
        #print("mean:"+str(np.mean(dst)))
        #print("std:"+str(np.std(dst)))
        return dst

    def canoniCorr(self):
        rmat = np.matrix(np.corrcoef(self.adatas).copy())
        rmatSize = len(rmat)
        r11 = rmat[0:rmatSize/2,0:rmatSize/2]
        r12 = rmat[rmatSize/2:rmatSize,0:rmatSize/2]
        r21 = r12.T
        r22 = rmat[rmatSize/2:rmatSize,rmatSize/2:rmatSize]
        #print(r11)
        #print(r11.shape)
        #print(r12)
        #print(r12.shape)
        #print(r21)
        #print(r21.shape)
        #print(r22)
        #print(r22.shape)

        r11 = np.linalg.inv(r11)
        r22 = np.linalg.inv(r22)
        
        ca = r11.dot(r12).dot(r22).dot(r21)
        #print(car)
        lam, v = np.linalg.eig(ca)
        #print(v)
        print(lam)
        va = v[:,0:1]
        vb = (r22.dot(r21).dot(va)/lam[0])

        print("user1")
        print(va)
        print(va.shape)

        print("user2")
        print(vb)
        print(vb.shape)

        adatasm = np.matrix(self.adatas).T
        rowSize, colSize = adatasm.shape
        fdata = adatasm[:,0:colSize/2]
        gdata = adatasm[:,colSize/2:colSize]

        print "r:"+str(rowSize)+", c:"+str(colSize)
        f = fdata.dot(va)
        g = gdata.dot(vb)

        F = np.squeeze(np.asarray(f))
        F1 = np.squeeze(np.asarray(fdata[:,0:1]))

        print "F:"+str(F)
        print F1

        #print(g.shape)
        #print fdata[:,0:1]
        F = np.squeeze(np.asarray(f))
        G = np.squeeze(np.asarray(g))
        for i in range(colSize/2):
            F1 = np.squeeze(np.asarray(fdata[:,i:i+1]))
            print("rf["+str(i)+"]:"+str(np.corrcoef(F,F1)[0][1]))
            G1 = np.squeeze(np.asarray(gdata[:,i:i+1]))
            print("rg["+str(i)+"]:"+str(np.corrcoef(G,G1)[0][1]))


def main():
    cancorr = CanCorr()
        

if __name__=='__main__':
    main()
