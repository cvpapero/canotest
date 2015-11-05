#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.cross_decomposition import CCA


def main():
    #X = [[2,5,7,9,8,4,2,6,3,6],[3,4,6,8,5,3,3,5,4,7]]
    #Y = [[4,6,8,8,7,2,3,7,5,8],[3,3,5,9,6,5,4,7,4,6]]
    X = [[73,74,86,74,80,78,86,82,87,80],[57,59,63,59,60,59,61,59,64,59]]
    Y = [[61,70,79,65,55,85,57,83,70,75],[48,48,52,48,42,58,48,52,52,52]]

    #cca = CCA(n_components=1)
    #cca.fit(X,Y)
    X_c = CCA(n_components=2).fit(X,Y).transform(X)

    print(X_c)
    #print(cca.fit(X, Y).x_loadings_)
    #print(Y_c)    

if __name__=='__main__':
    main()
