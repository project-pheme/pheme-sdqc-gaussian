'''
Created on 16 May 2015

@author: michal
'''
import getpass

#For EMNLP 2015 paper:
LABELS=[11, 12, 13]
#For further experiments:
#LABELS=[11, 12, 13, 14]

LABEL_POSITIVE=11

    
def ON_SERVER():
    return getpass.getuser() == "acp13ml"

def LOCALLY():
    return not ON_SERVER()