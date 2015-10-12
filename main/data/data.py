'''
Created on 14 May 2015

@author: michal
'''
import numpy as np
from numpy import linalg as LA

def foldsplitter(X, POSTPROCESSED_TASK_COLUMN_ID, train_set_sizes):
    '''
    For each task id (in column POSTPROCESSED_TASK_COLUMN_ID) take rows from number train_set_sizes up for testing, 
    and all other rows for training (so training consists of both other task ids and of rows from the same task id
    up to number train_set_sizes-1.
    
    TESTED
    '''
    folds=sorted(list(set(X[:, POSTPROCESSED_TASK_COLUMN_ID])))
    for fold in folds:
        for train_set_size in train_set_sizes:
            testfold2train=X[:, POSTPROCESSED_TASK_COLUMN_ID]==fold
            cnt=0
            for i, x in enumerate(testfold2train):
                if testfold2train[i]:
                    cnt+=1
                    if cnt>train_set_size:
                        testfold2train[i]=False
                    
            #print "x:", x
            remaining_train=X[:, POSTPROCESSED_TASK_COLUMN_ID]!=fold
            x=np.logical_or.reduce([testfold2train,remaining_train])
            #print "train:", x
            
            yield x, np.logical_not(x)

def normalize_time_for_tasks(X, header):
    '''
    Normalize tasks in X so that time starts at 0.
    '''
    try:
        timecol=header.index('time')
    except:
        timecol=header.index('timestamp')
    eventcol=header.index('event')
    for task in set(X[:, eventcol]):
        task_indices=X[:, eventcol]==task
        X[task_indices, timecol]-=np.min(X[task_indices, timecol])
        #Xtask[:, timecol]=Xtask[:, timecol]-np.min(Xtask[:, timecol])

def load_data(fname, labels_to_keep=None, normalize_text_rowwise=False, featuregroups=None):
    '''
    Load data from a csv file.
    '''
    #from main.utils.constants import EVENTCOL_RAW, RTTYPECOL_RAW, TEXTUPTOCOL_RAW, TIMESTAMPCOL_RAW
    X=np.loadtxt(fname, skiprows=1)
    header=open(fname).readline().split()
    
    #Xprocessed=np.hstack((X[:, TIMESTAMPCOL_RAW][:, None], X[:, :TEXTUPTOCOL_RAW], X[:, RTTYPECOL_RAW][:, None], X[:, EVENTCOL_RAW][:, None]))
    #index_vec=range(X.shape[0])
    #headerprocessed=[header[TIMESTAMPCOL_RAW]]+header[:TEXTUPTOCOL_RAW]+[header[RTTYPECOL_RAW], header[EVENTCOL_RAW]]
    
    Xprocessed=X[:,:-1]
    normalize_time_for_tasks(Xprocessed, header)
    
    headerprocessed=header[:-1]
    y=X[:, -1]
    
    if normalize_text_rowwise:
        #separately normalize each set from featuregroups_to_normalize
        for featuregroup in featuregroups:
            featureids=[i for i, h in enumerate(header) if featuregroup in h]
            for i, x in enumerate(X):
                xtmp=x[featureids]
                xtmp=xtmp/LA.norm(xtmp, 2)
                X[i,featureids]=xtmp
                
    if labels_to_keep!=None:
        Xprocessed=Xprocessed[np.logical_or.reduce([y==lbl for lbl in labels_to_keep]), :]
        y=y[np.logical_or.reduce([y==lbl for lbl in labels_to_keep])]
                
    index_vec=range(Xprocessed.shape[0])
    return Xprocessed, y, index_vec, headerprocessed

def load_data_oldexperiments(fname):
    '''
    Load data in a way consistent with old results (shown in old version of the arxiv paper).
    '''
    TEXTUPTOCOL_RAW=-3
    RTTYPECOL_RAW=-3
    QTYPECOL_RAW=-2
    EVENTCOL_RAW=-1
    
    X=np.loadtxt(fname, skiprows=1)
    header=open(fname).readline().split()
    
    Xprocessed=np.hstack((X[:, :TEXTUPTOCOL_RAW], X[:, RTTYPECOL_RAW][:, None], X[:, EVENTCOL_RAW][:, None]))
    y=X[:, QTYPECOL_RAW]
    index_vec=range(X.shape[0])
    headerprocessed=header[:TEXTUPTOCOL_RAW]+[header[RTTYPECOL_RAW], header[EVENTCOL_RAW]]
    return Xprocessed, y, index_vec, headerprocessed