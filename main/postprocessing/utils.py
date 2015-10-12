'''
Created on 25 May 2015

@author: michal
'''

import sys
import numpy as np
import sklearn.metrics
from os import listdir
from os.path import isfile, join

metric_varying_testset=lambda a, b, train_perc, max_train: sklearn.metrics.accuracy_score(a, b)
def metric_fixed_testset(a, b, train_perc, max_train): 
    start_index=max_train-train_perc
    return sklearn.metrics.accuracy_score(a[start_index:], b[start_index:])
#METRIC=metric_fixed_testset

def method_name_mapper(s):
    if s=="MostFrequentSingle":
        s="MajorityLabel"
    else:
        s=s.replace("Pooled", "Pooling")
        if "Pooling" not in s:
            s=s+"TargetRumourOnly"
    return s

def apply_metric_results(results, metric):
    for method in results.keys():
        max_train=max(results[method].keys())
        for train_perc in sorted(results[method].keys()):
            samples=len(results[method][train_perc])
            metric_val=np.mean([metric(a, b, train_perc=train_perc, max_train=max_train) for a, b in results[method][train_perc]])
            results[method][train_perc]=(metric_val, samples)

def display_results_table(results):
    for method in results.keys():
        print "method:", method
        for train_perc in sorted(results[method].keys()):
            print train_perc, ":", results[method][train_perc][0], results[method][train_perc][1]
    
def display_results_figure(results, METRIC):
    import pylab as pb
    color=iter(pb.cm.rainbow(np.linspace(0,1,len(results))))
    plots=[]
    for ind, method in enumerate(results.keys()):
        x=[]
        y=[]
        for train_perc in sorted(results[method].keys()):
            x.append(train_perc)
            y.append(results[method][train_perc][0])
        c=next(color)
        pi, = pb.plot(x, y, color=c)
        plots.append(pi)
    from matplotlib.font_manager import FontProperties
    fontP = FontProperties()
    fontP.set_size('small')
    pb.legend(plots, map(method_name_mapper, results.keys()), prop = fontP, bbox_to_anchor=(0.6, .65))
    pb.xlabel("#Tweets from target rumour for training")
    pb.ylabel("Accuracy")
    pb.title(METRIC.__name__)
    pb.savefig("incrementing_training_size.png")