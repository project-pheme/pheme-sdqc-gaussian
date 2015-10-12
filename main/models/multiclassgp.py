'''
Created on 7 Feb 2015

@author: michal
'''
import pickle
import GPy
import numpy as np
from collections import Counter
from scipy import cluster

RERUNS_LATENT_INPUTS=10
class MCGP(object):
    '''
    classdocs
    '''
    def __init__(self, kernel_constructor, labels, name=None, RANDOM_RESTARTS=-1, 
                 optimize=True, matrixify_y=False, num_inducing=None):
        '''
        Constructor
        '''
        self.k_constructor = kernel_constructor
        self.name = name
        self.RANDOM_RESTARTS = RANDOM_RESTARTS
        self.optimize = optimize
        self.matrixify_y = matrixify_y
        self.num_inducing=num_inducing
        
    def fit(self, X, y, optimize=True, matrixify_y=False):
        print "[MCGP.fit] Setting up model..."
        self.labels = list(set(y.flatten()))
        if self.matrixify_y:
            y=np.matrix(y[:, None])
        
        self.models = {}
        
        if self.num_inducing!=None:
            Z, distortion = cluster.vq.kmeans(X, self.num_inducing, iter=100)
        for label in self.labels:
            print "[MCGP.fit] label", label
            ytmp=y.copy()
            ytmp[ytmp!=label]=0
            ytmp[ytmp==label]=1
            
            if self.num_inducing!=None:
                for rerun in range(RERUNS_LATENT_INPUTS):
                    print "rerun:", rerun
                    try:
                        m=GPy.models.SparseGPClassification(X, ytmp[:, None], kernel=self.k_constructor(), Z=Z)
                        break
                    except:
                        Z, distortion = cluster.vq.kmeans(X, self.num_inducing, iter=100)
                        pass
            else:
                m=GPy.models.GPClassification(X, ytmp[:, None], kernel=self.k_constructor())
                
            #temporarily for debugging only:
            #m.kern.coregion.B=np.ones((2,2))
            #print "[MCGP.fit] before optimization m.kern.K(X):", m.kern.K(X)
            #KX=m.kern.K(X)
            #print "KX.shape:", KX.shape
            #print "numpy.linalg.matrix_rank(KX):", np.linalg.matrix_rank(KX)
            
            if self.optimize:
                print "[MCGP.fit] Optimizing..."
                if self.RANDOM_RESTARTS > 1:
                    m.optimize_restarts(messages=True, robust=True, 
                                        num_restarts=self.RANDOM_RESTARTS)
                else:
                    m.optimize(messages=True)
            #print "[MCGP.fit] after optimization m.kern.K(X):", m.kern.K(X)
            self.models[label]=m
        
    def predict(self, X):
        results_dict={}
        for label in self.labels:
            #print "[MCGP.predict] mean", mean
            mean, var = self.models[label].predict(X)
            results_dict[label]=mean
        Y=np.vstack(tuple([results_dict[label].T for label in self.labels]))
        result=map(lambda x: self.labels[x], Y.argmax(0))
        
        return result
    
    def predict_certainty(self, X):
        results_dict={}
        for label in self.labels:
            #print "[MCGP.predict] mean", mean
            mean, var = self.models[label].predict(X)
            results_dict[label]=mean
        Y=np.vstack(tuple([results_dict[label].T for label in self.labels]))
        result=map(lambda x: self.labels[x], Y.argmax(0))
        
        return result, results_dict
    
    def get_params(self, deep=False):
        return self.__dict__