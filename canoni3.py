#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import linalg 

def main():
    

    x1 = [73,74,86,74,80,78,86,82,87,80]
    x2 = [57,59,63,59,60,59,61,59,64,59]
    x3 = [61,70,79,65,55,85,57,83,70,75]
    x4 = [48,48,52,48,42,58,48,52,52,52]
    '''
    x1 = [2,5,7,9,8,4,2,6,3,6]
    x2 = [3,4,6,8,5,3,3,5,4,7]
    x3 = [4,6,8,8,7,2,3,7,5,8]
    x4 = [3,3,5,9,6,5,4,7,4,6]
    '''
    rmat = np.corrcoef([x1,x2,x3,x4])

    print(rmat)

    r11 = np.matrix([[1, rmat[0][1]],[rmat[0][1],1]])
    r12 = np.matrix([[rmat[0][2], rmat[0][3]],[rmat[1][2],rmat[1][3]]])
    r21 = r12.T
    r22 = np.matrix([[1, rmat[2][3]],[rmat[3][2],1]])

    print(r11)
    print(r12)
    print(r21)
    print(r22)

    r11 = linalg.inv(r11)
    r22 = linalg.inv(r22)

    car = r11.dot(r12).dot(r22).dot(r21)
    print(car)
    v = linalg.eig(car)

    #print(l)
    print(v) 
    #print(v[1,1]/v[0,1])

if __name__ == "__main__":
    main()
