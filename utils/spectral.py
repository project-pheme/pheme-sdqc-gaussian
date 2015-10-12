'''
Created on 7 Nov 2014

@author: michal
'''

def parse_spectral_cluster_dictionary(fname):
    word2cl = {}
    with open(fname) as f:
        for l in f:
            lspl = l.split()
            word2cl[lspl[0]] = (lspl[1], float(lspl[2]))
    return word2cl