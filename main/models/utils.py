'''
Created on 4 Feb 2015

@author: michal
'''

import sklearn.metrics
from main.utils.constants import LABELS

def print_metrics(true, predicted):
    f1 = sklearn.metrics.f1_score(true, predicted)#, pos_label=11)
    acc = sklearn.metrics.accuracy_score(true, predicted)
    prec = sklearn.metrics.precision_score(true, predicted)#, pos_label=11)
    recall = sklearn.metrics.recall_score(true, predicted)#, pos_label=11)
    print "accuracy:", acc
    print "f1:", f1
    print "precision:", prec
    print "recall:", recall
    print "Confusion matrix:"
    print sklearn.metrics.confusion_matrix(true, predicted)#, labels=LABELS)
    
def print_metrics_multiclass(true, predicted):
#    f1 = sklearn.metrics.f1_score(true, predicted, pos_label=11)
    acc = sklearn.metrics.accuracy_score(true, predicted)
#    prec = sklearn.metrics.precision_score(true, predicted, pos_label=11)
#    recall = sklearn.metrics.recall_score(true, predicted, pos_label=11)
    print "accuracy:", acc
#    print "f1:", f1
#    print "precision:", prec
#    print "recall:", recall
    print "Confusion matrix:"
    print sklearn.metrics.confusion_matrix(true, predicted, labels=LABELS)
    
def filter_methods(METHODNAMES_IN, METHODS_IN, methodnames):
    print "[filter_methods] Before Filtering: ", METHODNAMES_IN
    METHODS=[]
    METHODNAMES=[]
    for methodname in methodnames.split(","):
        try:
            ind = METHODNAMES_IN.index(methodname)
            METHODS += [METHODS_IN[ind]]
            METHODNAMES += [METHODNAMES_IN[ind]]
        except:
            pass
    print "[filter_methods] After Filtering: ", METHODNAMES
    return METHODNAMES, METHODS