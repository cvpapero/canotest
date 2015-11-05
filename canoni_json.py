#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import math
import json
import numpy


class CanCorr():

    def __init__(self):
        self.winSize = 30

        self.jsonInput()
        self.dataAlignment()
        self.canoniCorr()

    def jsonInput(self):
        f = open('test1014.json', 'r');
        jsonData = json.load(f)
        #print json.dumps(jsonData, sort_keys = True, indent = 4)
        f.close()

        self.dataSize = len(jsonData[0]["datas"])
        print ("dataSize:"+str(self.dataSize))
        self.jdatas = []
        for user in jsonData:
            #angle
            datas = []
            for j in range(self.dataSize):
                datas.append(self.scale(user["datas"][j]["data"]))
            self.jdatas.append(datas)
        #print(self.jdatas)
        #print(udatas[1][0][0])

    def dataAlignment(self):
        self.adatas = []
        self.range = self.dataSize-self.winSize+1
        for user in self.jdatas:
            adata = []
            for i in range(self.range):
                data = []
                for w in range(self.winSize):
                    data.extend(user[w+i])
                self.adatas.append(data)
            #self.adatas.append(adata)
        #print(self.adatas)
        #print(self.adatas[0][1])
        #print(self.adatas[0][2])
        #print(self.adatas[1][0])
        #print(self.adatas[1][1])
        #print(self.adatas[1][2])

    def scale(self, arr):
        dst = []
        m = numpy.mean(arr)
        s = numpy.std(arr)
        if s != 0.0:
            dst = numpy.array([(arr[i] - m)/s for i in range(len(arr))])
        #print("mean:"+str(numpy.mean(dst)))
        #print("std:"+str(numpy.std(dst)))
        return dst

    def canoniCorr(self):
        rmat = numpy.matrix(numpy.corrcoef(self.adatas).copy())
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

        r11 = numpy.linalg.inv(r11)
        r22 = numpy.linalg.inv(r22)
        
        ca = r11.dot(r12).dot(r22).dot(r21)
        #print(car)
        lam, v = numpy.linalg.eig(ca)
        #print(v)
        print(lam)
        va = v[:,0:1]
        print("r22:"+str(r22.shape)+", r21:"+str(r21.shape)+", va:"+str(va.shape))
        
        vb = (r22.dot(r21).dot(va)/lam[0])

        #vb = cb.dot(va)
        #print(cb.shape)
        #print(va.shape)        
        

        #print(lam)

        print("user1")
        print(va)
        print(va.shape)

        print("user2")
        print(vb)
        print(vb.shape)

        
def main():
    cancorr = CanCorr()
        

if __name__=='__main__':
    main()
