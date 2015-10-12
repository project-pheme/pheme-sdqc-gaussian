'''
Created on 23 Mar 2015

@author: michal
'''
from collections import Counter
from main.utils.utils import store, model_output_path
from main.experiment.utils import print_mcgp_method
import numpy as np
    
class Experiment(object):
    '''
    
    '''
    def __init__(self, X, y, index_vec, train_set_ratios, FOLDTORUN, 
                 summarize_labels, splitter, EVALUATION_MEASURES, 
                 METHODNAMES, METHODS, 
                 METHODNAMESSINGLETASK, METHODSSINGLETASK, print_metrics,
                 header,
                 RANDOM_RESTARTS=-1, results={}, store_models=None,
                 filter_retweets=True):
        '''
        Constructor
        '''
        
        self.X = X
        self.y = y
        self.index_vec = index_vec
        
        self.METHODNAMES = METHODNAMES
        self.METHODS = METHODS
        self.METHODNAMESSINGLETASK = METHODNAMESSINGLETASK
        self.METHODSSINGLETASK = METHODSSINGLETASK
        
        self.FOLDTORUN = FOLDTORUN
        self.splitter = splitter
        self.EVALUATION_MEASURES=EVALUATION_MEASURES
        
        self.summarize_labels = summarize_labels
        self.print_metrics = print_metrics
        self.results = results
        self.store_models=store_models
        self.header=header
        self.POSTPROCESSED_TASK_COLUMN_ID=header.index("event")
        
        self.METHODNAMES_ALL = self.METHODNAMES+self.METHODNAMESSINGLETASK
        
        self.filter_retweets = filter_retweets

    def run(self):
        for foldind, (train, test) in enumerate(self.splitter):
            print "[ExperimentLgcp.run] Fold:", foldind#, "train:", train, "test:", test, "self.X:", self.X, "self.y:", self.y
            if self.FOLDTORUN==-1 or self.FOLDTORUN==foldind:
                
                d={}
                d['multi']=(self.X[train, :], self.X[test, :], self.y[train], self.y[test], 
                            self.METHODNAMES, 
                            self.METHODS)
                d['single']=(self.X[train, :][self.X[train][:,self.POSTPROCESSED_TASK_COLUMN_ID]==self.X[test, :][0,self.POSTPROCESSED_TASK_COLUMN_ID]], 
                             self.X[test, :], 
                             self.y[train][self.X[train, :][:,self.POSTPROCESSED_TASK_COLUMN_ID]==self.X[test, :][0,self.POSTPROCESSED_TASK_COLUMN_ID]], 
                             self.y[test],
                             self.METHODNAMESSINGLETASK, 
                             self.METHODSSINGLETASK)
                
                for k, v in d.items():
                    X_train, X_test, y_train, y_test, METHODNAMES, METHODS = v
                    
                    if self.filter_retweets:
                        RTTYPECOL_PROCESSED=[ind for ind, h in enumerate(self.header) if h=="parent_type" or h=="parent_alg_type" or h=="is_simple_retweet"]#"parent" in h and "type" in h]
                        RTTYPECOL_PROCESSED=RTTYPECOL_PROCESSED[0]#assume we found exactly one needed index 
                        print "[load_data] len(X_train) before filtering out simple RT:", len(X_train)
                        y_train=y_train[X_train[:, RTTYPECOL_PROCESSED]!=1]
                        X_train=X_train[X_train[:, RTTYPECOL_PROCESSED]!=1, :]
                        print "[load_data] len(X_train) after filtering out simple RT:", len(X_train)
                                        
                    print "[ExperimentLgcp.run] method type:", k
                    print "[ExperimentLgcp.run] self.summarize_labels(y_train):", self.summarize_labels(y_train)
                    print "[ExperimentLgcp.run] self.summarize_labels(y_test):", self.summarize_labels(y_test)
                
                    for methodname, method_constructor in zip(METHODNAMES, METHODS):
                        print "[ExperimentLgcp.run] Method:", methodname
                        method = method_constructor()
                        result = self.evaluate_method(X_train, X_test, y_train, y_test, method, 
                                                      summarize_kernel=False)
                        self.results[methodname] = self.results.get(methodname, [])+[result]
                        #summarize_kernel(kmat, y_train=y_train, y_test=y_test, indices_train=self.index_vec[train], 
                        #                 indices_test=self.index_vec[test], header=methodname+" "+str(foldind), 
                        #                 method=method, X_test=X_test)
                        if self.store_models!=None:
                            method.train_indices=train
                            method.test_indices=test
                            store(model=method, path=model_output_path(self.store_models, methodname, foldind))

    def evaluate_method(self, X_train, X_test, y_train, y_test, method, summarize_kernel):
        method.fit(X_train, y_train)
        y_mean = method.predict(X_test)
        print "y_predicted:"+",".join(map(str, y_mean))
        print "y_true:"+",".join(map(str, y_test))
        self.print_metrics(y_test, y_mean)
        
        #Code below is just for printing the model
        print_mcgp_method(method, self.header)
        
        results=[EVALUATION_MEASURE(y_test, y_mean) for EVALUATION_MEASURE in self.EVALUATION_MEASURES]
        return results
    
    def summarize(self):
        print "[Experiment.summarize]"
        print "method", "mean", "std", "sample"
        import sys
        print >> sys.stderr, "FOLDTORUN: "+str(self.FOLDTORUN)+":"+str(self.results)
        for ind, metric in enumerate(self.EVALUATION_MEASURES):
            #print "[summarize] metric:", metric.__name__
            for key in self.METHODNAMES_ALL:
                value = map(lambda x: x[ind], self.results[key])
                print key, np.mean(value), np.std(value), len(value)